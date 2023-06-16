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
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer.data)
    if id:
        if request.method == "GET":
            all_plans = WeekPlan.objects.filter(user_id=user_id)

            min_date = request.GET.get("min_date", None)
            if min_date is not None:
                all_plans = all_plans.filter(monday_position__gte=min_date)
            max_date = request.GET.get("max_date", None)
            if max_date is not None:
                all_plans = all_plans.filter(monday_position__lte=max_date)

            serializer = WeekPlanSerializer(all_plans, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == "POST":
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
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "PUT", "DELETE"])
def week_plan_single(request, id):
    token = decrypt(request.headers.get("Authorization").split()[1].encode(), user_salt)
    all_users = User.objects.all()
    serializer_all = UserSerializer(all_users, many=True)
    user_id = checkToken(token, serializer_all.data)
    if id:
        try:
            target = WeekPlan.objects.get(pk=id)
        except WeekPlan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serializer = WeekPlanSerializer(target)
            if serializer.data["user_id"] == user_id:
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif request.method == "PUT":
            target_ser = WeekPlanSerializer(target).data
            if target_ser["user_id"] == user_id:
                target_ser = WeekPlanSerializer(target).data
                created_at = target_ser["created_at"]
                updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S").replace(" ", "T").replace("/", "-")
                serializer = WeekPlanSerializer(
                    target,
                    data={
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
            serializer = WeekPlanSerializer(target)
            if serializer.data["user_id"] == user_id:
                target.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)
