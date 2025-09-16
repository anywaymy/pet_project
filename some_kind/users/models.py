from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=24, unique=True)
    email = models.EmailField(max_length=40, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="users_images", null=True, blank=True)