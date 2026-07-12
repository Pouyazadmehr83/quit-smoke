from rest_framework import serializers
from .models import FinancialGoal


class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = (
            'id', 'title', 'target_amount_toman', 'is_active',
            'is_achieved', 'achieved_at', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_achieved', 'achieved_at', 'created_at', 'updated_at')


class GoalProgressSerializer(serializers.Serializer):
    """خروجی محاسبه‌ی پیشرفت هدف - مستقیماً از دیکشنری سرویس ساخته می‌شود."""
    goal_id = serializers.IntegerField()
    title = serializers.CharField()
    target_amount_toman = serializers.IntegerField()
    current_saved_toman = serializers.DecimalField(max_digits=14, decimal_places=0)
    remaining_amount_toman = serializers.DecimalField(max_digits=14, decimal_places=0)
    progress_percent = serializers.FloatField()
    estimated_days_remaining = serializers.IntegerField(allow_null=True)
    is_achieved = serializers.BooleanField()
