from django.urls import path
from .views import StreakLeaderboardView, SavingsLeaderboardView

urlpatterns = [
    path('streaks/', StreakLeaderboardView.as_view(), name='leaderboard-streaks'),
    path('savings/', SavingsLeaderboardView.as_view(), name='leaderboard-savings'),
]
