# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   urls.py
# -----------------------------------------------------------

from django.urls import path
from .views import *
from .views import MyTokenObtainPairView 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

#Routing API requests to functions
urlpatterns = [
    path('records/<str:pk>/', getRecord, name='record'),
    path('records/', getRecords, name='records'),
    path('record/search/', findDocument, name='find'),
    path('record/new/', newRecord, name='new'),
    path('record/take/', takeRecord, name='take'),
    path('record/leave/', leaveRecord, name='take'),
    path('record/delete/', deleteRecord, name='delete'),
    path('record/state/change/', changeState, name='step'),
    path('vcs/', getCollections, name='vcs'),
    path('vc/add/record/', addRecordToVC, name='vc_add'),
    path('vc/remove/record/', removeRecordFromVC, name='vc_add'),
    path('vc/<str:pk>/', downloadRecordsOfVc, name='vc'),
    path('vc/clear/all/', clearVC, name='vc_clear'),
    path('donators/', getDonators, name='donators'),
    path('routes/', getRoutes, name='routes'),
    path('profiles/import/', getImportProfiles, name='import_profiles'),
    path('profiles/export/', getExportProfiles, name='export_profiles'),
    path('user/records/', getUsersRecords, name='records'),
    path('user/history/', getUsersHistoryRecords, name='records'),
    path('user/statistics/', userStatistics, name='user_statistics'),
    path('admin/statistics/', adminStatistics, name='admin_statistics'),
    path('admin/record/state/change/', adminChangeState, name='change'),
    path('user/password/change/', changePassword, name='change_user_password'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]