# Generated by Django 5.0.1 on 2024-02-11 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_comment_commented_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
    ]