from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SmokingProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """سریالایزر ثبت‌نام کاربر جدید با ایمیل و رمز عبور."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'display_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'display_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class SmokingProfileSerializer(serializers.ModelSerializer):
    price_per_cigarette = serializers.ReadOnlyField()
    daily_saving_amount = serializers.ReadOnlyField()

    class Meta:
        model = SmokingProfile
        fields = (
            'id', 'brand_name', 'pack_price_toman', 'cigarettes_per_pack',
            'cigarettes_per_day', 'quit_start_date',
            'price_per_cigarette', 'daily_saving_amount',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
