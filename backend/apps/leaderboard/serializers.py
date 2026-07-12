from rest_framework import serializers


class LeaderboardEntrySerializer(serializers.Serializer):
    """یک ردیف از جدول لیدربورد - یا بر اساس استریک یا بر اساس پول پس‌انداز شده."""
    rank = serializers.IntegerField()
    display_name = serializers.CharField()
    value = serializers.DecimalField(max_digits=14, decimal_places=0)
    is_current_user = serializers.BooleanField()
