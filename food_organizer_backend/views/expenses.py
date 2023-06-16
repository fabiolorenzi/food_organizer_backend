from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..serializers.expense_serializer import ExpenseSerializer
from ..tools.security import decrypt, checkToken
from ..models.user import User
from ..models.expense import Expense
from datetime import datetime
from setting_data import user_salt


@api_view(["GET", "POST"])
def expense_list(request):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer.data)
    if id:
        if request.method == "GET":
            all_plans = Expense.objects.filter(user_id=user_id)

            min_date = request.GET.get("min_date", None)
            if min_date is not None:
                all_plans = all_plans.filter(shopping_date__gte=min_date)
            max_date = request.GET.get("max_date", None)
            if max_date is not None:
                all_plans = all_plans.filter(shopping_date__lte=max_date)

            serializer = ExpenseSerializer(all_plans, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == "POST":
            serializer = ExpenseSerializer(data={
                "user_id": user_id,
                "title": request.data["title"],
                "description": request.data["description"],
                "price": request.data["price"],
                "currency": request.data["currency"],
                "shopping_date": request.data["shopping_date"],
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
def expense_single(request, id):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer_all = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer_all.data)
    if id:
        try:
            target = Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = ExpenseSerializer(target)
            if serializer.data["user_id"] == user_id:
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif request.method == "PUT":
            target_ser = ExpenseSerializer(target).data
            if target_ser["user_id"] == user_id:
                target_ser = ExpenseSerializer(target).data
                created_at = target_ser["created_at"]
                updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                serializer = ExpenseSerializer(
                    target,
                    data={
                        "user_id": user_id,
                        "title": request.data["title"],
                        "description": request.data["description"],
                        "shopping_date": request.data["shopping_date"],
                        "price": request.data["price"],
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
            serializer = ExpenseSerializer(target)
            if serializer.data["user_id"] == user_id:
                target.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)
