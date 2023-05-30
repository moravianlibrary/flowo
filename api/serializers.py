# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   serializers.py
# -----------------------------------------------------------

# Import necessary modules
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Donator, ExportProfile, ImportProfile, Record, VirtualCollection

# Define a serializer for the Record model
class RecordSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField to customize the output of certain fields
    user = serializers.SerializerMethodField()  
    state = serializers.SerializerMethodField()
    vc = serializers.SerializerMethodField()
    ocr = serializers.SerializerMethodField()
    imprep = serializers.SerializerMethodField()
    # Customize datetime fields
    datetime_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    datetime_updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # Use the preprocess.progress field as a read-only source for progress
    progress = serializers.CharField(source='preprocess.progress', read_only=True)

    # Define the model and all fields for the serializer
    class Meta:
        model = Record
        fields = '__all__'

    # Override the to_representation method to format datetime fields as strings
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['datetime_created'] = instance.datetime_created.strftime("%Y-%m-%d %H:%M:%S")
        data['datetime_updated'] = instance.datetime_updated.strftime("%Y-%m-%d %H:%M:%S")
        return data
    
    # Define methods to get the username, state name, virtual collections, ocr, and imprep fields for a record
    def get_user(self, record):
        return record.user.username if record.user else None
    def get_state(self, record):
        return record.state.name if record.state else None
    def get_vc(self, record):
        return [vc.name for vc in record.vc.all()] if record.vc.exists() else None
    def get_ocr(self, record):
        return "True" if record.ocr else "False"
    def get_imprep(self, record):
        return "True" if record.imprep else "False"

# Define a serializer for all records
class AllRecordsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    process = serializers.SerializerMethodField()
    # Customize datetime fields
    datetime_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    datetime_updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    # Define the model and fields for the serializer
    class Meta:
        model = Record
        fields = ['uuid', 'name', 'barcode', 'datetime_created', 'datetime_updated', 'state', 'process', 'user']

    # Override the to_representation method to format datetime fields as strings
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['datetime_created'] = instance.datetime_created.strftime("%Y-%m-%d %H:%M:%S")
        data['datetime_updated'] = instance.datetime_updated.strftime("%Y-%m-%d %H:%M:%S")
        return data

    # Define methods to get the username, state name, and process name for a record
    def get_user(self, record):
        return record.user.username if record.user else None
    def get_state(self, record):
        return record.state.name if record.state else None
    
    # Define a method to return the process name based on the process value
    def get_process(self, record):
        match record.process:
            case 0:
                return "Scan"
            case 1:
                return "Crop"
            case 2:
                return "Imprep"
            case 3:
                return "OCR"
            case 4:
                return "PA Import"
            case 5:
                return "PA Meta"
            case 6:
                return "PA Export"
            case 7:
                return "Archive"
            case _:
                return "Unknown"
    
# Define a serializer for all virtual collections
class VirtualCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualCollection
        fields = '__all__'

# Define a serializer for number of records from each virtual collection
class VirtualCollectionNumOfRecords(VirtualCollectionSerializer):
    record_count = serializers.SerializerMethodField()

    class Meta(VirtualCollectionSerializer.Meta):
        fields = ('vc_id', 'name', 'record_count')

    def get_record_count(self, obj):
        return obj.record_set.count()

# Define a serializer for all import profiles
class ImportProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model= ImportProfile
        fields = '__all__'

# Define a serializer for all export porfiles
class ExportProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model= ExportProfile
        fields = '__all__'

# Define a serializer for all donators
class DonatorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Donator
        fields = '__all__'