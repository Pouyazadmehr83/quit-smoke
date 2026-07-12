from django.contrib import admin
from .models import DailyCheckIn, StreakSummary


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'is_smoke_free', 'created_at')
    list_filter = ('is_smoke_free',)
    search_fields = ('user__email',)


@admin.register(StreakSummary)
class StreakSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'total_smoke_free_days', 'total_money_saved')
    search_fields = ('user__email',)
