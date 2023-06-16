from django.db import models


class Product(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=25)
    expire_date = models.DateField()
    remaining = models.FloatField()
    measure_unit = models.CharField(max_length=5)
    quantity_alarm = models.BooleanField()
    quantity_alarm_threshold = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
