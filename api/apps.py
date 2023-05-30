# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   apps.py - basic app settings template
# -----------------------------------------------------------

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
