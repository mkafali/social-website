# Generated by Django 5.0.1 on 2024-02-11 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commented_by',
        ),
    ]
