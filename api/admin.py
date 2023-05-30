# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   admin.py
# -----------------------------------------------------------

from django.contrib import admin
from .models import *

# Models that are shown in the administator's interface
admin.site.register(Record)
admin.site.register(State)
admin.site.register(VirtualCollection)
admin.site.register(ProcessType)
admin.site.register(Process)
admin.site.register(ScanningDevice)
admin.site.register(ImportProfile)
admin.site.register(ExportProfile)
admin.site.register(Donator)