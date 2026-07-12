"""
مدل‌های پیگیری روزانه - ثبت اینکه کاربر در یک روز مشخص سیگار کشیده یا نه،
و محاسبه‌ی استریک (روزهای پاکی متوالی) و کل پول پس‌انداز شده.
"""
from django.db import models
from django.utils import timezone


class DailyCheckIn(models.Model):
    """
    ثبت روزانه‌ی وضعیت کاربر.
    هر کاربر برای هر تاریخ فقط یک رکورد دارد (unique_together).
    is_smoke_free=True یعنی آن روز سیگار نکشیده (پاک بوده).
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='checkins',
        verbose_name='کاربر'
    )
    date = models.DateField(default=timezone.localdate, verbose_name='تاریخ')
    is_smoke_free = models.BooleanField(verbose_name='پاک بوده؟')
    note = models.CharField(max_length=255, blank=True, verbose_name='یادداشت اختیاری')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ثبت روزانه'
        verbose_name_plural = 'ثبت‌های روزانه'
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        status = 'پاک' if self.is_smoke_free else 'لغزش'
        return f'{self.user.email} - {self.date} - {status}'


class StreakSummary(models.Model):
    """
    خلاصه‌ی وضعیت فعلی کاربر - یک رکورد به‌ازای هر کاربر که هر بار با چک‌این جدید
    آپدیت می‌شود. این جدول برای جلوگیری از محاسبه‌ی سنگین در هر درخواست (cache شده) است.

    current_streak: روزهای پاکی متوالی فعلی (از آخرین لغزش تا امروز)
    longest_streak: بیشترین استریک ثبت‌شده در طول تاریخ کاربر
    total_smoke_free_days: مجموع کل روزهای پاکی (نه فقط استریک فعلی)
    total_money_saved: مجموع پول پس‌انداز شده بر اساس total_smoke_free_days
    last_relapse_date: تاریخ آخرین لغزش (برای شروع مجدد شمارش استریک)
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='streak_summary',
        verbose_name='کاربر'
    )
    current_streak = models.PositiveIntegerField(default=0, verbose_name='استریک فعلی (روز)')
    longest_streak = models.PositiveIntegerField(default=0, verbose_name='بیشترین استریک')
    total_smoke_free_days = models.PositiveIntegerField(default=0, verbose_name='کل روزهای پاکی')
    total_money_saved = models.DecimalField(
        max_digits=14, decimal_places=0, default=0,
        verbose_name='کل پول پس‌انداز شده (تومان)'
    )
    last_relapse_date = models.DateField(null=True, blank=True, verbose_name='تاریخ آخرین لغزش')
    last_checkin_date = models.DateField(null=True, blank=True, verbose_name='تاریخ آخرین ثبت')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'خلاصه استریک'
        verbose_name_plural = 'خلاصه استریک‌ها'

    def __str__(self):
        return f'{self.user.email} - استریک: {self.current_streak} روز'
