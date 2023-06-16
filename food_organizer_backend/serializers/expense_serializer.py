from rest_framework import serializers
from ..models.expense import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            "id",
            "user_id",
            "title",
            "description",
            "price",
            "shopping_date",
            "created_at",
            "updated_at"
        )
