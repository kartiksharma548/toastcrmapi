from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
   
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('register', views.register, name='register'),
    path('getLead/<int:userid>', views.getLead, name='getLead'),
    path('updateLead/<int:id>', views.updateLead, name='updateLead'),
    path('getStatuses', views.getStatuses, name='getStatuses'),
    path('getSubStatuses/<int:substatus_id>', views.getSubStatuses, name='getSubStatuses'),
    path('createNote', views.postNote, name='createNote'),
    path('getNotes/<int:lead_id>', views.getNotes, name='getNotes'),
    path('updateNote/<int:id>', views.updateNote, name='updateNote'),
    path('deleteNote/<int:id>', views.deleteNote, name='deleteNote'),
    path('getCancelledStatuses', views.getCancelledStatuses, name='deleteNote'),
    path('schedule', views.ScheduleAPI.as_view()),
    path('schedule/<int:id>', views.ScheduleAPI.as_view()),
    path('getLeadChartData/<int:userid>', views.getLeadChartData, name='getLeadChartData'),
    path('getClientConversionData/<int:userid>', views.getClientConversionData, name='getClientConversionData'),
    path('updateUserProfile/<int:userid>', views.updateUserProfile, name='updateUserProfile'),
    path('changeStatus', views.changeStatus),
   
    
]
