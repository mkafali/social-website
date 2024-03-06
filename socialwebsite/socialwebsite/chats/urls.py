from django.urls import path
from . import views

urlpatterns = [
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('messenger/', views.messenger, name='messenger'),
    path('conversation/<str:username>/', views.conversation, name='conversation'),
    path('delete_message/<str:username>/<slug:message_slug>/', views.delete_message, name='delete_message'),
    

]