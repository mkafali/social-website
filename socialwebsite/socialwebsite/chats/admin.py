from django.contrib import admin
from .models import Chat, MessagesOfUser
# Register your models here.


admin.site.register(Chat)
admin.site.register(MessagesOfUser)