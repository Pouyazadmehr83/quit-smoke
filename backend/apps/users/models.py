"""
مدل کاربر سفارشی (احراز هویت با ایمیل) + پروفایل سیگار کشیدن کاربر
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator


class UserManager(__import__('django.contrib.auth.base_user', fromlist=['BaseUserManager']).BaseUserManager):
    """مدیر کاربر که به‌جای username از email استفاده می‌کند."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('ایمیل الزامی است')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    کاربر سفارشی - ورود با ایمیل به‌جای نام کاربری.
    فیلد username را غیرفعال نگه می‌داریم تا تداخلی با AbstractUser پیش نیاید
    اما عملاً برای لاگین استفاده نمی‌شود.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    display_name = models.CharField(max_length=100, blank=True, verbose_name='نام نمایشی')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.display_name or self.email


class SmokingProfile(models.Model):
    """
    پروفایل سیگارکشیدن کاربر - اطلاعاتی که برای محاسبه پس‌انداز لازم است.
    هر کاربر می‌تواند پروفایل خودش را آپدیت کند (مثلا اگر برند سیگار تغییر کرد).
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='smoking_profile',
        verbose_name='کاربر'
    )
    brand_name = models.CharField(max_length=150, verbose_name='برند سیگار', help_text='مثلا وینستون اولترا')
    pack_price_toman = models.PositiveIntegerField(
        verbose_name='قیمت پاکت (تومان)',
        validators=[MinValueValidator(1000)],
        help_text='قیمت یک پاکت سیگار به تومان'
    )
    cigarettes_per_pack = models.PositiveSmallIntegerField(
        default=20,
        verbose_name='تعداد سیگار در هر پاکت'
    )
    cigarettes_per_day = models.PositiveSmallIntegerField(
        verbose_name='تعداد سیگار مصرفی روزانه (قبل از ترک)',
        help_text='میانگین تعداد سیگار در روز قبل از شروع ترک'
    )
    quit_start_date = models.DateField(
        default=timezone.localdate,
        verbose_name='تاریخ شروع ترک'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پروفایل سیگار'
        verbose_name_plural = 'پروفایل‌های سیگار'

    def __str__(self):
        return f'{self.user.email} - {self.brand_name}'

    @property
    def price_per_cigarette(self) -> float:
        """قیمت هر عدد سیگار بر اساس قیمت پاکت."""
        if self.cigarettes_per_pack == 0:
            return 0
        return self.pack_price_toman / self.cigarettes_per_pack

    @property
    def daily_saving_amount(self) -> float:
        """مقدار پولی که هر روز پاکی صرفه‌جویی می‌شود."""
        return self.price_per_cigarette * self.cigarettes_per_day
