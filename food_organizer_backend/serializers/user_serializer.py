from rest_framework import serializers
from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "auth_from",
            "auth_until",
            "failed_attempts",
            "blocked_until",
            "created_at",
            "updated_at"
        ]
