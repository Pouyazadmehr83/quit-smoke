from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer, SmokingProfileSerializer
from .models import SmokingProfile

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """گرفتن JWT با ایمیل به‌جای username (username_field را override می‌کنیم)."""
    username_field = User.USERNAME_FIELD


class LoginView(TokenObtainPairView):
    """ورود کاربر با ایمیل و رمز عبور؛ خروجی access و refresh token."""
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    """ثبت‌نام کاربر جدید."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """دریافت و ویرایش اطلاعات کاربر فعلی."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SmokingProfileView(APIView):
    """
    دریافت و ساخت/ویرایش پروفایل سیگار کاربر فعلی.
    هر کاربر فقط یک پروفایل دارد (OneToOne) - GET/PUT/PATCH روی همان رکورد.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, 'smoking_profile', None)
        if not profile:
            return Response(
                {'detail': 'پروفایل سیگار هنوز ثبت نشده است.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(SmokingProfileSerializer(profile).data)

    def post(self, request):
        if hasattr(request.user, 'smoking_profile'):
            return Response(
                {'detail': 'پروفایل سیگار از قبل وجود دارد. برای ویرایش از PUT استفاده کنید.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SmokingProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        profile = getattr(request.user, 'smoking_profile', None)
        if not profile:
            return Response(
                {'detail': 'پروفایلی برای ویرایش وجود ندارد.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SmokingProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
