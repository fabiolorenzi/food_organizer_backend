from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..serializers.product_serializer import ProductSerializer
from ..tools.security import decrypt, checkToken
from ..models.user import User
from ..models.product import Product
from datetime import datetime
from setting_data import user_salt


@api_view(["GET", "POST"])
def product_list(request):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer.data)
    if id:
        if request.method == "GET":
            all_plans = Product.objects.filter(user_id=user_id)
            serializer = ProductSerializer(all_plans, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == "POST":
            serializer = ProductSerializer(data={
                "user_id": user_id,
                "name": request.data["name"],
                "position": request.data["position"],
                "expire_date": request.data["expire_date"],
                "remaining": request.data["remaining"],
                "measure_unit": request.data["measure_unit"],
                "quantity_alarm": request.data["quantity_alarm"],
                "quantity_alarm_threshold": request.data["quantity_alarm_threshold"],
                "created_at": datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-"),
                "updated_at": datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "PUT", "DELETE"])
def product_single(request, id):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer_all = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer_all.data)
    if id:
        try:
            target = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = ProductSerializer(target)
            if serializer.data["user_id"] == user_id:
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif request.method == "PUT":
            target_ser = ProductSerializer(target).data
            if target_ser["user_id"] == user_id:
                target_ser = ProductSerializer(target).data
                created_at = target_ser["created_at"]
                updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                serializer = ProductSerializer(
                    target,
                    data={
                        "user_id": user_id,
                        "name": request.data["name"],
                        "position": request.data["position"],
                        "expire_date": request.data["expire_date"],
                        "remaining": request.data["remaining"],
                        "measure_unit": request.data["measure_unit"],
                        "quantity_alarm": request.data["quantity_alarm"],
                        "quantity_alarm_threshold": request.data["quantity_alarm_threshold"],
                        "created_at": created_at,
                        "updated_at": updated_at
                    }
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif request.method == "DELETE":
            serializer = ProductSerializer(target)
            if serializer.data["user_id"] == user_id:
                target.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)
