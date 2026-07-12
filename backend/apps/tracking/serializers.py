from rest_framework import serializers
from .models import DailyCheckIn, StreakSummary


class DailyCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyCheckIn
        fields = ('id', 'date', 'is_smoke_free', 'note', 'created_at')
        read_only_fields = ('id', 'created_at')


class CheckInCreateSerializer(serializers.Serializer):
    """سریالایزر ورودی برای ثبت چک‌این - تاریخ پیش‌فرض امروز است."""
    date = serializers.DateField(required=False)
    is_smoke_free = serializers.BooleanField()
    note = serializers.CharField(required=False, allow_blank=True, max_length=255)


class StreakSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakSummary
        fields = (
            'current_streak', 'longest_streak', 'total_smoke_free_days',
            'total_money_saved', 'last_relapse_date', 'last_checkin_date', 'updated_at'
        )
