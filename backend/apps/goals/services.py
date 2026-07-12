"""
سرویس محاسبه‌ی پیشرفت هدف مالی بر اساس پس‌انداز فعلی و نرخ روزانه‌ی پس‌انداز کاربر.
"""
import math
from decimal import Decimal

from apps.tracking.services import get_user_streak_summary


def calculate_goal_progress(user, goal) -> dict:
    """
    محاسبه‌ی درصد پیشرفت و تخمین روزهای باقی‌مانده تا رسیدن به هدف مالی.

    اگر کاربر هیچ پروفایل سیگاری ثبت نکرده باشد یا نرخ پس‌انداز روزانه صفر باشد،
    days_remaining را None برمی‌گردانیم (یعنی غیرقابل تخمین).
    """
    summary = get_user_streak_summary(user)
    current_saved = summary.total_money_saved
    target = Decimal(goal.target_amount_toman)

    progress_percent = float(min(current_saved / target * 100, 100)) if target > 0 else 0
    remaining_amount = max(target - current_saved, Decimal('0'))

    profile = getattr(user, 'smoking_profile', None)
    daily_rate = Decimal(str(profile.daily_saving_amount)) if profile else Decimal('0')

    days_remaining = None
    if daily_rate > 0 and remaining_amount > 0:
        days_remaining = math.ceil(remaining_amount / daily_rate)
    elif remaining_amount <= 0:
        days_remaining = 0

    return {
        'goal_id': goal.id,
        'title': goal.title,
        'target_amount_toman': goal.target_amount_toman,
        'current_saved_toman': current_saved,
        'remaining_amount_toman': remaining_amount,
        'progress_percent': round(progress_percent, 1),
        'estimated_days_remaining': days_remaining,
        'is_achieved': current_saved >= target,
    }
