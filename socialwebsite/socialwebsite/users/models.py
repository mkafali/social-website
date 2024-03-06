from django.db import models
from django.conf import settings
# Create your models here.
from posts.models import Post, Comment
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/',verbose_name="Profile Photo", blank=True)
    bio = models.TextField(max_length=100, blank=True)
    private = models.BooleanField(default=False,blank=True)
    liked_posts = models.ManyToManyField(Post, related_name='like',blank=True)
    comments = models.ManyToManyField(Comment, related_name='comments',blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    follows = models.ManyToManyField(User, related_name='follows', blank=True)
    blocked = models.ManyToManyField(User, related_name='blocked', blank=True)

    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User Profiles"

