from django.urls import path
from . import views

urlpatterns = [
    path('my_follow_notifications/', views.my_follow_notifications, name='my_follow_notifications'),
    path('accept_follow_request/<str:sender>/', views.accept_follow_request, name='accept_follow_request'),
    path('deny_follow_request/<str:sender>/', views.deny_follow_request, name='deny_follow_request'),
    path('undo_follow_request/<str:reciever>/', views.undo_follow_request, name='undo_follow_request'),
    


]