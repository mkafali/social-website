from django.db import models
from django.conf import settings
from django.utils.text import slugify
import time
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/', verbose_name='POSTS', blank=False)
    caption  = models.TextField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, blank=True)
    created = models.DateField(auto_now_add = True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    comments = models.ManyToManyField('posts.Comment', related_name='comments_of_post', blank=True)

    def __str__(self):
        photo_post_title = f"{self.user.username}" + f"{self.slug}"
        return photo_post_title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            slug_var = str(time.time())
            while len(slug_var) < 17:
                slug_var += '0'
            self.slug = slugify(slug_var)

        super().save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'PHOTO POSTS'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_by')
    body = models.TextField()
    created_date = models.DateField(auto_now_add = True)
    comment_slug = models.TextField(max_length=18,blank=True)
    
    
    def __str__(self):
        comment_title = f"{self.post.slug}/{self.commented_by.username}/{self.comment_slug}"
        return comment_title
    
    def save(self,*args,**kwargs):
        if not self.comment_slug:
            slug_var = str(time.time())
            while len(slug_var) < 17:
                slug_var += '0'
            self.comment_slug = slugify(slug_var)

        super().save(*args,**kwargs)

    
    
    