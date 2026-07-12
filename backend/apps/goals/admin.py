from django.contrib import admin
from .models import FinancialGoal


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'target_amount_toman', 'is_active', 'is_achieved')
    list_filter = ('is_active', 'is_achieved')
    search_fields = ('user__email', 'title')
