from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    reset_password = models.BooleanField(default=False)
