from django.db import models


class UserModel(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=100)