# Generated by Django 5.0.1 on 2024-02-11 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_alter_comment_comment_slug'),
        ('users', '0008_profile_liked_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='posts.comment'),
        ),
    ]
