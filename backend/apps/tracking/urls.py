from django.urls import path
from .views import CheckInView, TodayStatusView, StreakSummaryView

urlpatterns = [
    path('checkin/', CheckInView.as_view(), name='checkin'),
    path('today/', TodayStatusView.as_view(), name='today-status'),
    path('summary/', StreakSummaryView.as_view(), name='streak-summary'),
]
