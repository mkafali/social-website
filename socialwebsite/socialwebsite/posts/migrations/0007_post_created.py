# Generated by Django 5.0.1 on 2024-02-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_post_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]