from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..tools.security import crypt, decrypt
from ..models.user import User
from datetime import datetime
from setting_data import user_salt


@api_view(["GET", "POST"])
def users_list(request):
    if request.method == "GET":
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        username = request.data["username"]
        email = request.data["email"]
        password = crypt(request.data["password"], user_salt)
        created_at = datetime.now()
        auth_from = created_at
        auth_until = created_at
        failed_attempts = 0
        blocked_until = created_at
        updated_at = created_at
        serializer = UserSerializer(data={
            "username": username,
            "email": email,
            "password": password.decode(),
            "auth_from": auth_from,
            "auth_until": auth_until,
            "failed_attempts": failed_attempts,
            "blocked_until": blocked_until,
            "created_at": created_at,
            "updated_at": updated_at
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
