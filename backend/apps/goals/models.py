"""
مدل هدف‌گذاری مالی - کاربر یک هدف (مثلا خرید موتور با قیمت X تومان) تعریف می‌کند
و سیستم بر اساس پس‌انداز روزانه‌اش تخمین می‌زند چند روز دیگر به آن می‌رسد.
"""
from django.db import models
from django.utils import timezone


class FinancialGoal(models.Model):
    """
    هدف مالی کاربر. در هر لحظه کاربر می‌تواند چند هدف فعال داشته باشد،
    اما برای سادگی MVP، یک هدف «اصلی» (is_active) در نظر می‌گیریم که در داشبورد نشان داده می‌شود.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='کاربر'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان هدف', help_text='مثلا خرید موتور هوندا')
    target_amount_toman = models.PositiveBigIntegerField(verbose_name='هزینه‌ی هدف (تومان)')
    is_active = models.BooleanField(default=True, verbose_name='هدف فعال (اصلی)؟')
    is_achieved = models.BooleanField(default=False, verbose_name='رسیده به هدف؟')
    achieved_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ رسیدن به هدف')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'هدف مالی'
        verbose_name_plural = 'هدف‌های مالی'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.title} ({self.target_amount_toman:,} تومان)'
