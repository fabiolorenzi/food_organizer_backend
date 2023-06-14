from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..models.user import User


@api_view(["GET"])
def users_list(request):
    all_users = User.object.all()
    serializer = UserSerializer(all_users, many = True)
    return JsonResponse(serializer.data, safe=False)
