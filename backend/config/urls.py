from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="QuitSmoke API",
        default_version='v1',
        description="API پلتفرم ترک سیگار - محاسبه پس‌انداز و پیگیری روزهای پاکی",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/', include('apps.users.urls')),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Domain apps
    path('api/tracking/', include('apps.tracking.urls')),
    path('api/goals/', include('apps.goals.urls')),
    path('api/leaderboard/', include('apps.leaderboard.urls')),

    # API Docs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
