# Generated by Django 5.0.1 on 2024-02-11 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]