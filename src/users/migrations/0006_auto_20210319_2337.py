# Generated by Django 3.1.7 on 2021-03-19 20:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210319_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follow',
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
