from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.week_plan_serializer import WeekPlanSerializer
from ..tools.security import crypt, decrypt, checkToken
from ..models.week_plan import WeekPlan
from datetime import datetime, timedelta
from setting_data import user_salt


@api_view(["GET", "POST"])
def week_plan_list(request):
    if request.method == "GET":
        all_plans = WeekPlan.objects.all()
        serializer = WeekPlanSerializer(all_plans, many=True)
        return JsonResponse(serializer.data, safe=False)
