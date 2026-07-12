from django.urls import path
from .views import GoalListCreateView, GoalDetailView, ActiveGoalProgressView, GoalProgressView

urlpatterns = [
    path('', GoalListCreateView.as_view(), name='goal-list-create'),
    path('active/progress/', ActiveGoalProgressView.as_view(), name='goal-active-progress'),
    path('<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
    path('<int:pk>/progress/', GoalProgressView.as_view(), name='goal-progress'),
]
