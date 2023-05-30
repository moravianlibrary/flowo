# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   tasks.py
# -----------------------------------------------------------

# Import necessary modules
from celery import shared_task
from .proarc import *
import shutil
import requests
import json
import time
import os


from api.models import Process, Record, State, ProcessType
from api.proarc import newBatch

RopeRunning = False
all_done = True
# Defining the base URL for the API
rope_url = os.getenv("ROPE_URL")
listOfRopeTasks = {}

# Looping function for getting the state of all running Rope tasks
@shared_task
def requestRopeState():
    time.sleep(5)
    print("Watching state")
    # Access the global variable
    global listOfRopeTasks
    global RopeRunning
    global all_done
    # Loop until all tasks are finished or terminated
    RopeRunning = True
    while True:
        # Send a POST request to the API with the list of task IDs
        response = requests.post(rope_url + 'state', json={'taskIDs': list(listOfRopeTasks.keys())})
        # Parse the JSON response
        try:
            json_data = json.loads(response.text)
        except json.decoder.JSONDecodeError as e:
            print(f'Error parsing JSON response: {e}')
            time.sleep(1)
            break
        # Initialize a flag to track whether all tasks are finished or terminated
        all_done = True
        # Loop through the list of tasks in the JSON data
        for task_data in json_data:
            print(task_data)
            uuid = listOfRopeTasks[task_data['taskID']]
            # Check if the 'Status' key in the task's JSON data is 'Finished' or 'Terminated'
            if task_data['Status'] not in ['Finished', 'Terminated', 'Crashed', 'NotFound']:
                record = Record.objects.get(uuid=uuid)
                record.preprocess.progress = task_data['State']
                print("Aktualni stave je:",record.preprocess.progress)
                record.preprocess.save()
                # If the task is not finished or terminated, set the flag to False
                all_done = False
                # Break out of the loop
                break
            elif task_data['Status'] == 'Finished':
                record = Record.objects.get(uuid=uuid)
                state = State.objects.get(pk=1)
                record.preprocess.progress = task_data['State']
                record.preprocess.state = State.objects.get(pk=3)
                record.state = state
                record.process = record.process + 1
                record.save()
                if record.ocr:
                    record.state = State.objects.get(pk=2)
                    record.ocr = False
                    record.save()
                    time.sleep(5)
                    runOCR(record.directory, uuid, 2)
                elif record.process == 3:
                    record.process = record.process + 1
                print(record.process)
                record.user = None
                record.save()
                record.preprocess.save()
                print("Konecny stav je:",record.preprocess.progress)
                # Remove the task ID from the original list if it is finished
                del listOfRopeTasks[task_data['taskID']]
                print('Process',{task_data['taskID']},'has finished in Rope.')
            elif task_data['Status'] in ['Terminated', 'Crashed']:
                record = Record.objects.get(uuid=uuid)
                record.preprocess.progress = task_data['State']
                if record.ocr:
                    record.ocr = False
                if record.process == 2:
                    record.process = record.process + 1
                record.process = record.process + 1
                record.preprocess.state = State.objects.get(pk=3)
                record.preprocess.save()
                record.user = None
                record.save()
                del listOfRopeTasks[task_data['taskID']]
                print('Process',{task_data['taskID']},'has been terminated in Rope.')
        if all_done:
            # If all tasks are finished or terminated, break out of the loop
            break
        else:
            # Wait for some time before checking the status again
            time.sleep(5)
    RopeRunning = False


            
# Run the Imagepreperation task in Rope
@shared_task
def runImprep(input, uuid):
    global rope_url
    global all_done
    global RopeRunning
    # Define the API endpoint path
    endpoint = "apiaction"

    modifyPath = input
    print("Cesta:", modifyPath)
    if modifyPath.startswith("/nf/norske_fondy/"):
        modifyPath = modifyPath.replace("/nf/norske_fondy/", "", 1)

    data = {
        'filename': modifyPath,
        'engineId': 0,
        'type': 'imgprep'
    }

    url = f"{rope_url}{endpoint}"
    response = requests.post(url, data)
    print("URL:", url)
    print("Response:", response)
    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        process_id = json_data[0]
        listOfRopeTasks[process_id] = uuid
        all_done = False

        if not RopeRunning:
            print("Running a requestState")
            requestRopeState()
        return(process_id)
    else:
        return ("Failed to run Imprep. Code:", response.status_code)


# Run the OCR task in Rope
@shared_task
def runOCR(input, uuid, engineId):
    global rope_url
    global all_done
    global RopeRunning

    endpoint = "apiaction"

    modifyPath = input
    if modifyPath.startswith("/nf/norske_fondy/"):
        modifyPath = modifyPath.replace("/nf/norske_fondy/", "", 1)

    data = {
        'filename': modifyPath,
        'engineId': engineId,
        'type': 'pero'
    }

    url = f"{rope_url}{endpoint}"

    record = Record.objects.get(uuid=uuid)
    if record.ocr:
        record.process += 1
        record.ocr = False
    state = State.objects.get(pk=2)
    record.state = state
    print("Status", record.state)
    record.save()

    response = requests.post(url, data)

    if response.status_code == 200:
        json_data = json.loads(response.content.decode('utf-8'))
        process_id = json_data[0]
        listOfRopeTasks[process_id] = uuid
        all_done = False

        if not RopeRunning:
            requestRopeState()
        return(process_id)
    else:
        return ("Failed to run OCR. Code:", response.status_code)

# Move directory from src_path to dst_path, when startPA is true, run ProArc import as well
@shared_task
def moveDir(src_path, dst_path, uuid, startPA):
    if not os.path.exists(src_path):
        return("Source directory does not exist")
    elif os.path.exists(dst_path):
        return("Destination directory already exists")
    else:
        try:
            shutil.copytree(src_path, dst_path)
            print("Directory copied successfully from", src_path, "to", dst_path)

            # Perform verification by comparing file sizes
            for root, dirs, files in os.walk(src_path):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    dst_file_path = os.path.join(dst_path, os.path.relpath(src_file_path, src_path))
                    if os.path.getsize(src_file_path) != os.path.getsize(dst_file_path):
                        raise Exception("File size does not match: " + src_file_path)

            shutil.rmtree(src_path)
            print("Original directory", src_path, "removed successfully")
            record = Record.objects.get(uuid=uuid)
            record.directory = dst_path
            record.save()
            time.sleep(1)

            if startPA:
                profile = record.import_profile.value
                device = record.scanning_device.device_id
                dir_path = "disk_proarc_import/" + uuid
                cookies = login()
                response = newBatch(uuid, dir_path, profile, device, cookies)
            else:
                record.process = record.process + 1
                record.save()
                     
            return("Success")
        except Exception as e:
            return("Error:", str(e))
        
# Run ProArc export and set donator
@shared_task
def proarcExport(uuid, donator, archive, kwis, policy):
    pid = "uuid:"+uuid
    kwisExported = True
    archiveExported = True
    donatorSet = True
    cookies = login()
    
    donatorSet = setDonator(donator, pid, cookies)

    if kwis:
        if policy:
            kwisExported = exportKwis(pid, "public", cookies)
        else:
            kwisExported = exportKwis(pid, "private", cookies)
    
    if archive:
        archiveExported = exportArchive(pid, "STT", cookies)

    record = Record.objects.get(uuid=uuid)
    record.state = State.objects.get(pk=3)
    record.export.state = State.objects.get(pk=3)
    record.process += 1
    record.user = None
    record.save()
    record.export.save()
    return True if kwisExported and archiveExported and donatorSet else False