from django.db import models
from django.conf import settings
from django.utils.text import slugify
import time
from django.contrib.auth.models import User
# Create your models here.

class MyFollowNotification(models.Model):
    follow_reciever = models.ForeignKey(User, related_name= 'follow_reciever',on_delete=models.CASCADE)
    follow_sender = models.ManyToManyField(User, related_name='follow_sender', blank=True)

    def __str__(self):
        title = f"{self.follow_reciever.username}'s follow requests"
        return title
    

