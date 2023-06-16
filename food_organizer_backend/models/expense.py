from django.db import models


class Expense(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    currency = models.CharField(max_length=3)
    shopping_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
