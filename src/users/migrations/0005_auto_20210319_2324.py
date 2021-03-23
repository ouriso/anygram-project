# Generated by Django 3.1.7 on 2021-03-19 20:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210317_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
