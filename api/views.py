# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   views.py
# -----------------------------------------------------------

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
import json
from .models import *
from .proarc import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
import xml.etree.ElementTree as ET
from django.db.models import Q
from .tasks import *
import csv
import os
from django.contrib.auth import authenticate
from datetime import datetime, timedelta



#main functions

"""
Get a token for a given user and add additional data to the token.

Args:
    user: A User instance.

Returns:
    A token with the username, id, and is_superuser fields added.
"""
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['id'] = user.id
        token['is_superuser'] = user.is_superuser

        return token
    

"""
Return JWT tokens (access and refresh) for specific user based on username and password.
"""
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""
A function that returns a list of available routes for the API.

Parameters:
    - request: A GET HTTP request object.

Returns:
    - A Response object with the available routes in JSON format.
"""
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/records/<str:pk>/',
        '/api/records/',
        '/api/record/search/',
        '/api/record/new/',
        '/api/record/take/',
        '/api/record/leave/',
        '/api/record/delete/',
        '/api/record/state/change/',
        '/api/vcs/',
        '/api/vc/add/record/',
        '/api/vc/remove/record/',
        '/api/vc/<str:pk>/',
        '/api/vc/clear/all/',
        '/api/donators/',
        '/api/profiles/import/',
        '/api/profiles/export/',
        '/api/user/records/',
        '/api/user/history/',
        '/api/user/statistics/',
        '/api/user/password/change/',
        '/api/admin/statistics/',
        '/api/admin/record/state/change/'
    ]
    return Response(routes)


"""
A function that returns a list of all records in the database as JSON.

Parameters:
    - request: A GET HTTP request object.

Returns:
    - A Response object with the list of all records in JSON format.
"""
@api_view(['GET'])
def getRecords(request):
    records = Record.objects.all()
    serializer = AllRecordsSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCollections(request):
    """
    A function that returns a list of all virtual collections in the database and the number of records in each collection as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A Response object with the list of virtual collections and the number of records in each collection in JSON format.
    """
    collections = VirtualCollection.objects.all()
    serializer = VirtualCollectionNumOfRecords(collections, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getImportProfiles(request):
    """
    A function that returns a list of all import profiles in the database as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A Response object with the list of all import profiles in JSON format.
    """
    profiles = ImportProfile.objects.all()
    serializer = ImportProfilesSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getExportProfiles(request):
    """
    A function that returns a list of all export profiles in the database as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A Response object with the list of all export profiles in JSON format.
    """
    profiles = ExportProfile.objects.all()
    serializer = ExportProfilesSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRecord(request, pk):
    """
    A function that returns a single record with a given UUID as JSON.

    Parameters:
        - request: A GET HTTP request object.
        - pk: The UUID of the record to retrieve.

    Returns:
        - A JSON object representing the requested record.
    """
    record = Record.objects.get(uuid=pk)
    serializer = RecordSerializer(record, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUsersRecords(request):
    """
    A function that returns a all record for a specific user as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A JSON object representing the requested records.
    """
    user = request.user
    user = User.objects.get(username=user)
    records = Record.objects.filter(user=user)
    serializer = AllRecordsSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUsersHistoryRecords(request):
    """
    A function that returns a history of procesess for a specific user as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A JSON object representing the requested processes.
    """
    user = request.user
    user = User.objects.get(username=user)
    records = Record.objects.filter(
        Q(processes__user=user) & ~Q(user=user)
    ).distinct()
    serializer = AllRecordsSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def userStatistics(request):
    """
    A function that returns a user statistics from past week as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A JSON object representing statistics from single user from past week.
    """
    user = request.user
    print(user)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    processes_count = user.process_set.filter(datetime_created__range=[week_start, week_end]).count()
    records_count = user.record_set.filter(datetime_created__range=[week_start, week_end]).count()
    return JsonResponse({'processes_count': processes_count, 'records_count': records_count})


@api_view(['GET'])
def adminStatistics(request):
    """
    A function that returns a admin statistics from past week as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A JSON object representing statistics from all users from past week.
    """
    all_users = User.objects.all()
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    stats = []
    for user in all_users:
        processes_count = user.process_set.filter(datetime_created__range=[week_start, week_end]).count()
        records_count = user.record_set.filter(datetime_created__range=[week_start, week_end]).count()
        stats.append({'user': user.username, 'processes_count': processes_count, 'records_count': records_count})
    return JsonResponse({'stats': stats})


@api_view(['GET'])
def getDonators(request):
    """
    A function that returns a list of all donators in the database as JSON.

    Parameters:
        - request: A GET HTTP request object.

    Returns:
        - A Response object with the list of all donators in JSON format.
    """
    donators = Donator.objects.all()
    serializer = DonatorSerializer(donators, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def takeRecord(request):
    """
    A function that sets the user ID of a record to the ID of a given user.

    Args:
        request: A HTTP request object containing a JSON body with the user ID and UUID of the record.

    Returns:
        A JSON object representing the updated record.
    """
    data = json.loads(request.body)
    userid = data.get('userid')
    user = User.objects.get(id=userid)
    uuid = data.get('uuid')
    print(uuid)
    if uuid:
        try:
            record = Record.objects.get(uuid=uuid)
            record.user_id = user.id
            print(user)
            record.save()
            serializer = RecordSerializer(record, many=False)
            return Response(serializer.data)
        except Record.DoesNotExist:
            pass
    return Response({'fail': uuid})



@api_view(['POST'])
def leaveRecord(request):
    """
    A function that removes the user ID from a record with a given UUID and returns the updated record as JSON.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object representing the updated record.
    """
    data = json.loads(request.body)
    uuid = data.get('uuid')
    if uuid:
        try:
            record = Record.objects.get(uuid=uuid)
            record.user_id = None
            record.save()
            serializer = RecordSerializer(record, many=False)
            return Response(serializer.data)
        except Record.DoesNotExist:
            pass
    return Response({'fail': uuid})

@api_view(['POST'])
def addRecordToVC(request):
    """
    A function that adds a VC to specific record.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object representing the updated record.
    """
    data = json.loads(request.body)
    uuid = data.get('uuid')
    vc_id = data.get('vc_id')
    if uuid != None and vc_id != None:
        vc = VirtualCollection.objects.get(pk=vc_id)
        record = Record.objects.get(uuid=uuid)
        
        if record.vc.filter(pk=vc_id).exists():
            return Response({'message': 'Virtual collection already exists in record.'}, status=400)
        
        record.vc.add(vc)
        record.save()
        serializer = RecordSerializer(record)
        return Response(serializer.data)
    
    return Response({'message': 'Invalid request data.'}, status=400)



@api_view(['POST'])
def removeRecordFromVC(request):
    """
    A function that removes a VC to specific record.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object representing the updated record.
    """
    data = json.loads(request.body)
    uuid = data.get('uuid')
    vc_id = data.get('vc_id')

    if uuid != None and vc_id != None:
        vc = VirtualCollection.objects.get(pk=vc_id)
        record = Record.objects.get(uuid=uuid)
        
        if not record.vc.filter(pk=vc_id).exists():
            return Response({'message': 'Virtual collection does not exist in record.'}, status=400)
        
        record.vc.remove(vc)
        record.save()
        serializer = RecordSerializer(record)
        return Response(serializer.data)
    
    return Response({'message': 'Invalid request data.'}, status=400)


@api_view(['POST'])
def clearVC(request):
    """
    A function that removes all records from a specific VC.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object stating if clear was successful.
    """
    data = json.loads(request.body)
    vc_id = data.get('vc_id')
    vc = VirtualCollection.objects.get(pk=vc_id)
    if vc_id != None and vc != None:
        vc.record_set.clear()
        return Response({'success': True})
    
    return Response({'success': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    """
    A function that changes a user's password.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object stating if password change was successful.
    """
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    user = authenticate(username=request.user.username, password=current_password)
    if user is None:
        return JsonResponse({'success': False, 'message': 'Incorrect current password'})

    if new_password != confirm_password:
        return JsonResponse({'success': False, 'message': 'New passwords do not match'})

    user.set_password(new_password)
    user.save()

    return JsonResponse({'success': True, 'message': 'Password changed successfully'})



@api_view(['GET'])
def downloadRecordsOfVc(request, pk):
    """
    A function that downloads the UUIDs of all records belonging to a given Virtual Collection as a CSV file.

    Parameters:
        - request: A GET HTTP request object.
        - pk: The UUID of the Virtual Collection whose records will be downloaded.

    Returns:
        - A Response containing error message about not found records for given Virtual Collection
        - A HTTP response with a CSV file attachment containing the UUIDs of all records belonging to the Virtual Collection.
    """
    virtual_collection = get_object_or_404(VirtualCollection, vc_id=pk)
    records = Record.objects.filter(vc=virtual_collection)

    record_ids = [record.uuid for record in records]
    if len(record_ids) <= 0:
        return Response('No records found for given virtual collection')
    
    record_ids_with_uuid = [f'uuid:{id}' for id in record_ids]

    filename = f"{virtual_collection.name}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    for record_id in record_ids_with_uuid:
        writer.writerow([record_id])

    return response



@api_view(['POST'])
def findDocument(request):
    """
    A function that searches for a record in a catalogue by barcode and returns a JSON object with the record's title and barcode.

    Parameters:
        - request: A POST HTTP request object.
        
    Returns:
        - A JSON object representing the requested record.
    """
    data = json.loads(request.body)
    barcode = data.get('barcode')
    try:
        if int(barcode) < 1000000:
            response_data = {'Error': barcode}
            return JsonResponse(response_data)
    except:
        response_data = {'Error': barcode}
        return JsonResponse(response_data)
    cookies = login()
    mods = catalogueSearch(cookies, barcode, "aleph_mzk01")
    mods2 = catalogueSearch(cookies, barcode, "aleph_mzk03")
    title = ""
    title2 = ""
    if mods:
        root = ET.fromstring(mods)
        title = root.find('.//{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title').text
        print(title)

    if mods2:
        root2 = ET.fromstring(mods2)
        title2 = root2.find('.//{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title').text

    data = {'title': {title, title2},
            'barcode': barcode,}
    return Response(data)


@api_view(['POST'])
def newRecord(request):
    """
    A function that searches for a record in a catalogue by barcode and creates a new record.

    Parameters:
        - request: A POST HTTP request object.
        
    Returns:
        - A JSON object representing the new record.
    """
    data = json.loads(request.body)
    user = request.user
    barcode = data.get('barcode')
    try:
        if int(barcode) < 1000000:
            response_data = {'Error': barcode}
            return JsonResponse(response_data)
    except:
        response_data = {'Error': barcode}
        return JsonResponse(response_data)
    cookies = login()
    mods = catalogueSearch(cookies, barcode, "aleph_mzk01")
    if not mods:
        mods = catalogueSearch(cookies, barcode, "aleph_mzk03")
    
    root = ET.fromstring(mods)
    title = root.find('.//{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title').text

    print(title)
    response = newObject(mods, cookies)

    print(response)

    pid = extract_pid(response)
    uuid = pid.split(':', 1)[1]

    state = State.objects.get(pk=1)
    stateDone = State.objects.get(pk=3)
    processType = ProcessType.objects.get(pk=1)
    process = Process.objects.create(process_type=processType, state=stateDone, user=user)
    process.save()
    path = os.getenv("PATH_TO_FLOWO_DIR")
    path = path + user.username + "/"

    if not os.path.exists(os.path.join(path, uuid)):
        os.makedirs(os.path.join(path, uuid))
        print("Directory", uuid, "created at", path)
    else:
        print("Directory", uuid, "already exists at", path)
    record = Record.objects.create(
        uuid=uuid,
        barcode=int(barcode),
        user=user,
        name=title,
        state=state,
        process=0,
        directory=os.path.join(path, uuid),
        create=process,
    )

    process.save()
    serializer = RecordSerializer(record, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteRecord(request):
    """
    A function that removes a record from the database and from the ProArc.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object stating if the deletion was successful.
    """
    data = json.loads(request.body)
    uuid = data.get('uuid')
    record = Record.objects.get(uuid=uuid)
    record.delete()
    response = deleteObject(uuid, login())
    record_exists = Record.objects.filter(uuid=uuid).exists()
    if not record_exists and response:
        return Response({'Success': True})
    return Response({'Success': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adminChangeState(request):
    """
    A function that changes the current process of given record - admin only.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object representing the changed record.
    """
    user = request.user
    uuid = request.data.get('uuid')
    note = request.data.get('note')
    newState = request.data.get('new_state')
    record = Record.objects.get(uuid=uuid)
    user = User.objects.get(username=user)
    if (0 <= int(newState) <= 7) and user.is_superuser:
        try:
            record.process = newState
            if record.note != note:
                record.note = note
            record.save()

        except Record.DoesNotExist:
            pass
    serializer = RecordSerializer(record, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changeState(request):
    """
    A function that changes the current process of given record to the next one.

    Parameters:
    - request: A POST HTTP request object.

    Returns:
    - A JSON object representing the changed record.
    """
    user = request.user
    uuid = request.data.get('uuid')
    newState = request.data.get('new_state')
    note = request.data.get('note')
    newDirPath = request.data.get('dirPath')      
    if uuid and newState != None:
        record = Record.objects.get(uuid=uuid)
        if newDirPath:
            record.directory = newDirPath
            record.save()
        print(record.directory)
        try:
            if (0 <= int(newState) <= 7) and user.id == record.user_id:  #only user which owns the record can change the state
                match int(newState):
                    case 0:
                        record.process = newState
                        record.save()
                    case 1:
                        response = ProcessCrop(uuid, user, newState, request)
                        if response:
                            return Response('NoScannerFound')
                    case 2:
                        processRope(uuid, user, newState)
                    case 5:
                        response = processImport(uuid, user, newState, request)
                        if response:
                            return Response('NoImportProfileFound')
                    case 6:
                        processMeta(uuid, user, newState, request)
                    case 7:
                        processExport(uuid, user, request)
        except Record.DoesNotExist:
            pass
        
        record = Record.objects.get(uuid=uuid)
        if record.note != note:
            record.note = note
            record.save()
        serializer = RecordSerializer(record, many=False)
        return Response(serializer.data)
    return Response(False)

#Helper function for creating new process objects
def createProcess(uuid, user, typePk, statePk):
    processType = ProcessType.objects.get(pk=typePk)
    processState = State.objects.get(pk=statePk)
    record = Record.objects.get(uuid=uuid)
    process = Process.objects.create(
        process_type=processType,
        record=record,
        user=user,
        state=processState
    )
    process.save()
    return process

#Process step from scanning to cropping
def ProcessCrop(uuid, user, newState, request):
    ocrState = request.data.get('ocr_state')
    imgState = request.data.get('img_state')
    scanner = request.data.get('scanner')
    if not scanner:
        return Response('NoScannerFound')
    record = Record.objects.get(uuid=uuid)
    process = createProcess(uuid, user, 2, 3)
    scanningDevice = ScanningDevice.objects.get(pk=scanner)
    record.scanning_device = scanningDevice
    record.scan = process
    state = State.objects.get(pk=1)
    record.state = state
    record.process = newState
    record.ocr = ocrState
    record.imprep = imgState
    record.user = None
    record.save()

#Process step from cropping to preprocessing
def processRope(uuid, user, newState):
    record = Record.objects.get(uuid=uuid)
    process = createProcess(uuid, user, 3, 2)
    record.preprocess = process
    if record.imprep:
        state = State.objects.get(pk=2)
        record.state = state
        record.process = newState
        process.save()
        record.save()
        runImprep.delay(record.directory, uuid)
    elif record.ocr:
        state = State.objects.get(pk=2)
        record.state = state
        record.process = newState
        record.save()
        process.save()
        runOCR.delay(record.directory, uuid, 2)
    else:
        state = State.objects.get(pk=1)
        record.state = state
        newState += 2
        record.process = newState
        processState = State.objects.get(pk=3)
        process.state = processState
        process.save()
        record.save()

#Process step from preprocessing to ProArc importing
def processImport(uuid, user, newState, request):
    selectedProfile = request.data.get('importProfile')
    if not selectedProfile or selectedProfile == "":
        print("Please select")
        return Response('NoImportProfileFound')
    importProfile = ImportProfile.objects.get(pk=selectedProfile)
    process = createProcess(uuid, user, 4, 2)
    state = State.objects.get(pk=2)
    record = Record.objects.get(uuid=uuid)
    record.meta = process
    record.user = None
    record.state = state
    record.import_profile = importProfile
    record.save()
    src_dir = record.directory
    
    dst_dir = os.getenv("PATH_TO_PA_IMPORT_DIR") +user.username+"/"+uuid
    response = moveDir.delay(src_dir, dst_dir, uuid, True)
    print(response)

#Process step from ProArc importing to editing metadata
def processMeta(uuid, user, newState, request):
    record = Record.objects.get(uuid=uuid)
    record.process += 1
    record.user = None
    record.meta.state = State.objects.get(pk=3)
    record.meta.save()
    record.save()

#Process step from editing metadata to exporting and archiving
def processExport(uuid, user, request):
    process = createProcess(uuid, user, 5, 2)
    archive = request.data.get('archive')
    kwis = request.data.get('kwis')
    policy = request.data.get('exportPolicy')
    donator = request.data.get('donator')
    record = Record.objects.get(uuid=uuid)
    record.state = State.objects.get(pk=2)
    record.export = process
    record.save()
    response = proarcExport.delay(uuid, donator, archive, kwis, policy)

    serializer = RecordSerializer(record, many=False)
    if response:
        return Response(serializer.data)
    return JsonResponse({'message': 'Process failed during export'})