"""
تست‌های واحد برای سرویس محاسبه‌ی استریک و پول پس‌انداز شده.
اجرا: docker compose exec backend python manage.py test apps.tracking
"""
from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import SmokingProfile
from apps.tracking.services import record_checkin, get_user_streak_summary, CheckInError

User = get_user_model()


class StreakCalculationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.profile = SmokingProfile.objects.create(
            user=self.user,
            brand_name='وینستون اولترا',
            pack_price_toman=150000,
            cigarettes_per_pack=20,
            cigarettes_per_day=10,  # نیم پاکت در روز => روزانه 75000 تومان
        )
        self.today = timezone.localdate()

    def test_daily_saving_amount_calculation(self):
        # 150000 / 20 = 7500 تومان هر سیگار؛ در روز 10 تا => 75000 تومان
        self.assertEqual(self.profile.daily_saving_amount, 75000)

    def test_smoke_free_day_increases_streak_and_savings(self):
        record_checkin(self.user, self.today, is_smoke_free=True)
        summary = get_user_streak_summary(self.user)

        self.assertEqual(summary.current_streak, 1)
        self.assertEqual(summary.total_smoke_free_days, 1)
        self.assertEqual(summary.total_money_saved, Decimal('75000'))

    def test_ten_smoke_free_days_savings(self):
        for i in range(10):
            record_checkin(self.user, self.today - timedelta(days=9 - i), is_smoke_free=True)

        summary = get_user_streak_summary(self.user)
        self.assertEqual(summary.current_streak, 10)
        self.assertEqual(summary.total_money_saved, Decimal('750000'))  # 10 * 75000

    def test_relapse_resets_current_streak_but_keeps_total_savings(self):
        record_checkin(self.user, self.today - timedelta(days=2), is_smoke_free=True)
        record_checkin(self.user, self.today - timedelta(days=1), is_smoke_free=True)
        record_checkin(self.user, self.today, is_smoke_free=False)

        summary = get_user_streak_summary(self.user)
        self.assertEqual(summary.current_streak, 0)
        self.assertEqual(summary.total_smoke_free_days, 2)
        self.assertEqual(summary.total_money_saved, Decimal('150000'))
        self.assertEqual(summary.last_relapse_date, self.today)

    def test_longest_streak_persists_after_relapse(self):
        for i in range(5):
            record_checkin(self.user, self.today - timedelta(days=9 - i), is_smoke_free=True)
        record_checkin(self.user, self.today - timedelta(days=4), is_smoke_free=False)
        for i in range(3):
            record_checkin(self.user, self.today - timedelta(days=2 - i), is_smoke_free=True)

        summary = get_user_streak_summary(self.user)
        self.assertEqual(summary.longest_streak, 5)
        self.assertEqual(summary.current_streak, 3)

    def test_duplicate_checkin_for_same_date_raises_error(self):
        record_checkin(self.user, self.today, is_smoke_free=True)
        with self.assertRaises(CheckInError):
            record_checkin(self.user, self.today, is_smoke_free=True)
