from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..tools.security import crypt, decrypt, checkToken
from ..models.user import User
from datetime import datetime, timedelta
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


@api_view(["GET", "PUT", "DELETE"])
def user_single(request, id):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    if checkToken(token, serializer.data):
        try:
            target = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = UserSerializer(target)
            return Response(serializer.data)
        elif request.method == "PUT":
            target_ser = UserSerializer(target).data
            username = request.data["username"]
            email = request.data["email"]
            password = crypt(request.data["password"], user_salt)
            auth_from = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            auth_until = (datetime.now() + timedelta(hours=24)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            failed_attempts = 0
            blocked_until = (datetime.now() - timedelta(hours=24)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            created_at = target_ser["created_at"]
            updated_at = auth_from
            serializer = UserSerializer(
                target,
                data={
                    "username": username,
                    "email": email,
                    "password": password.decode(),
                    "auth_from": auth_from,
                    "auth_until": auth_until,
                    "failed_attempts": failed_attempts,
                    "blocked_until": blocked_until,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
            )
            if serializer.is_valid():
                serializer.save()
                new_token = (
                        "id:" + str(serializer.data["id"]) +
                        ">>username:" + serializer.data["username"] +
                        ">>email:" + serializer.data["email"] +
                        ">>password:" + serializer.data["password"] +
                        ">>created_at:" + serializer.data["created_at"] +
                        ">>updated_at:" + updated_at +
                        ">>auth_from:" + serializer.data["auth_from"] +
                        ">>auth_until:" + serializer.data["auth_until"]
                )
                return JsonResponse({"token": crypt(new_token, user_salt).decode(), "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["PATCH"])
def user_login(request):
    email = request.data["email"]
    password = request.data["password"]
    all_users = User.objects.all()
    serializer_list = UserSerializer(all_users, many=True)
    index = 0
    while index < len(serializer_list.data):
        if email == serializer_list.data[index]["email"]:
            # The code below is to check if the user is blocked
            if serializer_list.data[index]["blocked_until"] > datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-"):
                return Response(status=status.HTTP_425_TOO_EARLY)

            # The code below is to check if the password is correct
            target = User.objects.get(id=int((serializer_list.data[index]["id"])))
            if password == decrypt(serializer_list.data[index]["password"].encode(), user_salt):
                failed_attempts = 0
                auth_from = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                auth_until = (datetime.now() + timedelta(hours=24)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                blocked_until = (datetime.now() - timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                updated_until = auth_from
                serializer = UserSerializer(
                    target,
                    data={"auth_from": auth_from, "auth_until": auth_until,"blocked_until": blocked_until, "failed_attempts": failed_attempts},
                    partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    new_token = (
                        "id:" + str(serializer_list.data[index]["id"]) +
                        ">>username:" + serializer_list.data[index]["username"] +
                        ">>email:" + serializer_list.data[index]["email"] +
                        ">>password:" + serializer_list.data[index]["password"] +
                        ">>created_at:" + serializer_list.data[index]["created_at"] +
                        ">>updated_at:" + updated_until +
                        ">>auth_from:" + auth_from +
                        ">>auth_until:" + auth_until
                    )
                    return JsonResponse({"token": crypt(new_token, user_salt).decode()})
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                failed_attempts = serializer_list.data[index]["failed_attempts"]
                blocked_until = serializer_list.data[index]["blocked_until"]
                if (failed_attempts + 1) >= 5:
                    # This code will block the user if he tried for more 5 times
                    blocked_until = (datetime.now() + timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                    failed_attempts = 0
                    serializer = UserSerializer(
                        target,
                        data={"blocked_until": blocked_until, "failed_attempts": failed_attempts},
                        partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    return Response(status=status.HTTP_403_FORBIDDEN)
                else:
                    failed_attempts = serializer_list.data[index]["failed_attempts"] + 1
                    serializer = UserSerializer(
                        target,
                        data={"blocked_until": blocked_until, "failed_attempts": failed_attempts},
                        partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    return Response(status=status.HTTP_403_FORBIDDEN)

        else:
            index += 1
    return Response(status=status.HTTP_404_NOT_FOUND)
