"""
لیست نفرات برتر - طبق تصمیم پروژه دو لیست جداگانه ارائه می‌شود:
1. برترین‌های استریک فعلی (بیشترین روزهای پاکی متوالی)
2. برترین‌های پول پس‌انداز شده (بیشترین مجموع صرفه‌جویی)
هیچ اطلاعات حساس کاربر (ایمیل) نمایش داده نمی‌شود؛ فقط display_name.
"""
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.tracking.models import StreakSummary
from .serializers import LeaderboardEntrySerializer

TOP_N = 20


def _build_entries(queryset, value_field, request_user_id):
    entries = []
    for rank, summary in enumerate(queryset, start=1):
        name = summary.user.display_name or summary.user.email.split('@')[0]
        entries.append({
            'rank': rank,
            'display_name': name,
            'value': getattr(summary, value_field),
            'is_current_user': summary.user_id == request_user_id,
        })
    return entries


class StreakLeaderboardView(APIView):
    """لیست برترین‌ها بر اساس بیشترین استریک فعلی (روزهای پاکی متوالی)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = StreakSummary.objects.select_related('user').filter(
            current_streak__gt=0
        ).order_by('-current_streak')[:TOP_N]

        entries = _build_entries(queryset, 'current_streak', request.user.id)
        return Response(LeaderboardEntrySerializer(entries, many=True).data)


class SavingsLeaderboardView(APIView):
    """لیست برترین‌ها بر اساس بیشترین پول پس‌انداز شده."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = StreakSummary.objects.select_related('user').filter(
            total_money_saved__gt=0
        ).order_by('-total_money_saved')[:TOP_N]

        entries = _build_entries(queryset, 'total_money_saved', request.user.id)
        return Response(LeaderboardEntrySerializer(entries, many=True).data)
