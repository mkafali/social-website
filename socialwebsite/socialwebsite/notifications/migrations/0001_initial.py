# Generated by Django 5.0.1 on 2024-02-19 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyFollowNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folllow_sender', models.ManyToManyField(blank=True, related_name='follow_sender', to=settings.AUTH_USER_MODEL)),
                ('follow_reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_reciever', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
