# Generated by Django 5.0.1 on 2024-02-13 13:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_profile_comments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
