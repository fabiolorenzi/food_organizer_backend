from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializer import UserSerializer
from ..serializers.week_plan_serializer import WeekPlanSerializer
from ..tools.security import decrypt, checkToken
from ..models.user import User
from ..models.week_plan import WeekPlan
from datetime import datetime
from setting_data import user_salt


@api_view(["GET", "POST"])
def week_plan_list(request):
    if request.method == "GET":
        all_plans = WeekPlan.objects.all()
        serializer = WeekPlanSerializer(all_plans, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        id = checkToken(token, serializer.data)
        if id:
            try:
                target = User.objects.get(pk=id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            user_id = UserSerializer(target).data["id"]
            serializer = WeekPlanSerializer(data={
                "user_id": user_id,
                "monday_position": request.data["monday_position"],
                "monday_breakfast": request.data["monday_breakfast"],
                "monday_lunch": request.data["monday_lunch"],
                "monday_dinner": request.data["monday_dinner"],
                "tuesday_breakfast": request.data["tuesday_breakfast"],
                "tuesday_lunch": request.data["tuesday_lunch"],
                "tuesday_dinner": request.data["tuesday_dinner"],
                "wednesday_breakfast": request.data["wednesday_breakfast"],
                "wednesday_lunch": request.data["wednesday_lunch"],
                "wednesday_dinner": request.data["wednesday_dinner"],
                "thursday_breakfast": request.data["thursday_breakfast"],
                "thursday_lunch": request.data["thursday_lunch"],
                "thursday_dinner": request.data["thursday_dinner"],
                "friday_breakfast": request.data["friday_breakfast"],
                "friday_lunch": request.data["friday_lunch"],
                "friday_dinner": request.data["friday_dinner"],
                "saturday_breakfast": request.data["saturday_breakfast"],
                "saturday_lunch": request.data["saturday_lunch"],
                "saturday_dinner": request.data["saturday_dinner"],
                "sunday_breakfast": request.data["sunday_breakfast"],
                "sunday_lunch": request.data["sunday_lunch"],
                "sunday_dinner": request.data["sunday_dinner"],
                "created_at": datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-"),
                "updated_at": datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
            })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)