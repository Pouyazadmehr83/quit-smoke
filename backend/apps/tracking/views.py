from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from .models import DailyCheckIn
from .serializers import (
    DailyCheckInSerializer, CheckInCreateSerializer, StreakSummarySerializer
)
from .services import record_checkin, get_user_streak_summary, has_checked_in_today, CheckInError


class CheckInView(APIView):
    """
    ثبت وضعیت روزانه (پاک بودی یا نه؟) و دریافت تاریخچه‌ی چک‌این‌ها.

    GET: لیست چک‌این‌های کاربر (صفحه‌بندی شده)
    POST: ثبت چک‌این جدید برای امروز (یا تاریخ مشخص‌شده)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        checkins = DailyCheckIn.objects.filter(user=request.user)[:30]
        return Response(DailyCheckInSerializer(checkins, many=True).data)

    def post(self, request):
        serializer = CheckInCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        date = data.get('date', timezone.localdate())

        try:
            checkin = record_checkin(
                user=request.user,
                date=date,
                is_smoke_free=data['is_smoke_free'],
                note=data.get('note', '')
            )
        except CheckInError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(DailyCheckInSerializer(checkin).data, status=status.HTTP_201_CREATED)


class TodayStatusView(APIView):
    """
    وضعیت امروز کاربر: آیا قبلا ثبت کرده؟ به همراه خلاصه‌ی استریک و پول پس‌انداز شده.
    این endpoint اصلی صفحه‌ی داشبورد است.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        summary = get_user_streak_summary(request.user)
        already_checked_in = has_checked_in_today(request.user)

        return Response({
            'already_checked_in_today': already_checked_in,
            'streak_summary': StreakSummarySerializer(summary).data,
        })


class StreakSummaryView(generics.RetrieveAPIView):
    """دریافت خلاصه‌ی استریک و پول پس‌انداز شده‌ی کاربر فعلی."""
    serializer_class = StreakSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_user_streak_summary(self.request.user)
