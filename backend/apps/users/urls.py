from django.urls import path
from .views import RegisterView, LoginView, MeView, SmokingProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('smoking-profile/', SmokingProfileView.as_view(), name='smoking-profile'),
]
