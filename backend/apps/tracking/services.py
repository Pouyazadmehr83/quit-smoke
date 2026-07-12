"""
سرویس محاسبه‌ی استریک (روزهای پاکی متوالی) و پول پس‌انداز شده.
این منطق عمداً از View ها جدا شده تا قابل تست و استفاده‌ی مجدد باشد
(مثلا توسط Celery task ایمیل روزانه در فاز بعد).
"""
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

from .models import DailyCheckIn, StreakSummary


class CheckInError(Exception):
    """خطای منطقی هنگام ثبت چک‌این (مثلا ثبت تکراری برای یک روز)."""
    pass


@transaction.atomic
def record_checkin(user, date, is_smoke_free: bool, note: str = '') -> DailyCheckIn:
    """
    ثبت وضعیت روزانه‌ی کاربر و آپدیت خلاصه‌ی استریک.

    منطق:
    - اگر چک‌این برای این تاریخ از قبل وجود دارد، خطا می‌دهیم (باید از update استفاده شود).
    - اگر پاک بوده: استریک فعلی +۱، کل روزهای پاکی +۱، پول پس‌انداز آپدیت می‌شود.
    - اگر لغزش داشته: استریک فعلی صفر می‌شود و last_relapse_date ثبت می‌شود.
      (توجه: لغزش، روزهای پاکی قبلی را از کارنامه‌ی کل پاک نمی‌کند - فقط استریک ریست می‌شود)
    """
    if DailyCheckIn.objects.filter(user=user, date=date).exists():
        raise CheckInError('برای این تاریخ قبلاً ثبت انجام شده است.')

    checkin = DailyCheckIn.objects.create(
        user=user, date=date, is_smoke_free=is_smoke_free, note=note
    )

    summary, _ = StreakSummary.objects.get_or_create(user=user)

    profile = getattr(user, 'smoking_profile', None)
    daily_saving = Decimal(str(profile.daily_saving_amount)) if profile else Decimal('0')

    if is_smoke_free:
        summary.current_streak += 1
        summary.total_smoke_free_days += 1
        summary.total_money_saved += daily_saving
        if summary.current_streak > summary.longest_streak:
            summary.longest_streak = summary.current_streak
    else:
        summary.current_streak = 0
        summary.last_relapse_date = date

    summary.last_checkin_date = date
    summary.save()

    return checkin


def get_user_streak_summary(user) -> StreakSummary:
    """گرفتن یا ساخت خلاصه‌ی استریک کاربر (برای کاربرانی که هنوز چک‌این نکرده‌اند)."""
    summary, _ = StreakSummary.objects.get_or_create(user=user)
    return summary


def has_checked_in_today(user) -> bool:
    """آیا کاربر برای امروز قبلا ثبت کرده است؟"""
    today = timezone.localdate()
    return DailyCheckIn.objects.filter(user=user, date=today).exists()
