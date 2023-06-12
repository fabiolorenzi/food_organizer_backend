from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)