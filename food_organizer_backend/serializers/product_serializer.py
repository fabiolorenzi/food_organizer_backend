from rest_framework import serializers
from ..models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "user_id",
            "name",
            "position",
            "expire_date",
            "remaining",
            "measure_unit",
            "quantity_alarm",
            "quantity_alarm_threshold",
            "quantity_alarm_active",
            "created_at",
            "updated_at"
        )
