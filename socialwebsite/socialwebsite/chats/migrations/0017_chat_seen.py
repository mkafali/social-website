# Generated by Django 5.0.1 on 2024-02-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0016_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='seen',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
