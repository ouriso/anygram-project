from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField(
        'self', symmetrical=False, related_name='+', blank=True
    )
