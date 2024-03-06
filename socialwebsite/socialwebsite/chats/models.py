from django.db import models
from django.conf import settings
from django.utils.text import slugify
import time
from django.contrib.auth.models import User

class Chat(models.Model):
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_by' ,on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name='sent_to', on_delete=models.CASCADE ,blank=False)
    content = models.TextField(blank=False)
    slug = models.SlugField(max_length=100, blank=True)
    seen = models.BooleanField(default=False,blank=True)

    def __str__(self):
        chat_title = f"{self.sent_by.username}-->{self.sent_to.username}/{self.slug}"
        return chat_title

    def save(self,*args,**kwargs):
        if not self.slug:
            message_time = str(time.time())
            while len(message_time) < 17:
                message_time += "0"
            self.slug = slugify(message_time)

        super().save(*args,**kwargs)


class MessagesOfUser(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE, blank=False)
    to_who = models.ManyToManyField(User, related_name='to_who', blank=False)
    message_content = models.ManyToManyField('chats.Chat', blank=True)

    def __str__(self):
        title = f"{self.owner.username}"
        return title
    
    