# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   models.py
# -----------------------------------------------------------

from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

#Creating database tables thanks to ORM
class State(models.Model):
    STATE_CHOICES = [
        ('waiting', 'Waiting'),
        ('running', 'Running'),
        ('done', 'Done'),
    ]
    name = models.CharField(max_length=7, choices=STATE_CHOICES)
    description = models.CharField(max_length=255, default="", blank=True)


class VirtualCollection(models.Model):
    vc_id = models.CharField(unique=True, primary_key=True, max_length=255)
    name = models.CharField(max_length=255)


class ScanningDevice(models.Model):
    device_id = models.CharField(max_length=43, validators=[MinLengthValidator(43)], unique=True, primary_key=True)
    name = models.CharField(max_length=255)


class ImportProfile(models.Model):
    value = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)

class ExportProfile(models.Model):
    value = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)


class Donator(models.Model):
    value = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="", blank=True)


class Record(models.Model):
    uuid = models.CharField(max_length=36, unique=True, primary_key=True, validators=[MinLengthValidator(36)])
    barcode = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    user = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL, blank=True)
    note = models.CharField(max_length=255, default="", blank=True)
    directory = models.CharField(max_length=255)
    vc = models.ManyToManyField(VirtualCollection)
    archive = models.BooleanField(default=True)
    imprep = models.BooleanField(default=True)
    ocr = models.BooleanField(default=True)
    ocr_engine = models.IntegerField(validators=[MaxValueValidator(6), MinValueValidator(0)], null=True, blank=True)
    process = models.IntegerField(default=0)
    batchId = models.IntegerField(blank=True, null=True)
    create = models.OneToOneField('Process', blank=True, on_delete=models.SET_NULL, null=True, related_name='create_id_of_record')
    scan = models.OneToOneField('Process', blank=True, on_delete=models.SET_NULL, null=True, related_name='scan_process_of_record')
    preprocess = models.OneToOneField('Process', blank=True, on_delete=models.SET_NULL, null=True, related_name='preprocess_id_of_record')
    meta = models.OneToOneField('Process', blank=True, on_delete=models.SET_NULL, null=True, related_name='meta_id_of_record')
    export = models.OneToOneField('Process', blank=True, on_delete=models.SET_NULL, null=True, related_name='export_id_of_record')
    public = models.BooleanField(default=False)
    scanning_device = models.ForeignKey(ScanningDevice, on_delete=models.SET_NULL, blank=True, null=True)
    import_profile = models.ForeignKey(ImportProfile, on_delete=models.SET_NULL, blank=True, null=True)
    export_profile = models.ForeignKey(ExportProfile, on_delete=models.SET_NULL, blank=True, null=True)
    donator = models.ForeignKey(Donator, on_delete=models.SET_NULL, null=True)


class ProcessType(models.Model):
    process_type_name = models.CharField(max_length=255)


class Process(models.Model):
    process_type = models.ForeignKey(ProcessType, blank=True, on_delete=models.PROTECT)
    record = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='processes')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    progress = models.CharField(max_length=255, blank=True, default="")
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, default="", blank=True)
