# Generated by Django 3.1.7 on 2021-03-17 20:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210316_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='_user_follow_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
