# Generated by Django 5.0.1 on 2024-02-09 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_time',
            field=models.TextField(blank=True),
        ),
    ]
