from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SmokingProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'display_name', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('display_name', 'first_name', 'last_name')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('email', 'display_name')


@admin.register(SmokingProfile)
class SmokingProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'brand_name', 'pack_price_toman', 'cigarettes_per_day', 'quit_start_date')
    search_fields = ('user__email', 'brand_name')
