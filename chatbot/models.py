from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    reset_password = models.BooleanField(default=False)


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    competency = models.CharField(max_length=255)

    def __str__(self):
        return self.name