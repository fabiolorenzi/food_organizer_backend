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
