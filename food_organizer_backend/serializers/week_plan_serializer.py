from rest_framework import serializers
from ..models.week_plan import WeekPlan


class WeekPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekPlan
        fields = (
            "id",
            "user_id",
            "monday_position",
            "monday_breakfast",
            "monday_lunch",
            "monday_dinner",
            "tuesday_breakfast",
            "tuesday_lunch",
            "tuesday_dinner",
            "wednesday_breakfast",
            "wednesday_lunch",
            "wednesday_dinner",
            "thursday_breakfast",
            "thursday_lunch",
            "thursday_dinner",
            "friday_breakfast",
            "friday_lunch",
            "friday_dinner",
            "saturday_breakfast",
            "saturday_lunch",
            "saturday_dinner",
            "sunday_breakfast",
            "sunday_lunch",
            "sunday_dinner",
            "created_at",
            "updated_at"
        )
