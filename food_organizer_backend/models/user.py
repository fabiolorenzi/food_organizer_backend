from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=500)
    auth_from = models.DateTimeField()
    auth_until = models.DateTimeField()
    failed_attempts = models.IntegerField()
    blocked_until = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
