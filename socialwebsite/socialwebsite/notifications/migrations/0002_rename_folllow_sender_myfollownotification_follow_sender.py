# Generated by Django 5.0.1 on 2024-02-19 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myfollownotification',
            old_name='folllow_sender',
            new_name='follow_sender',
        ),
    ]
