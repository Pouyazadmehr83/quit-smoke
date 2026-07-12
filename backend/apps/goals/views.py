from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import FinancialGoal
from .serializers import FinancialGoalSerializer, GoalProgressSerializer
from .services import calculate_goal_progress


class GoalListCreateView(generics.ListCreateAPIView):
    """لیست هدف‌های کاربر و ساخت هدف جدید."""
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # اگر هدف جدید فعال باشد، بقیه هدف‌ها را غیرفعال می‌کنیم (فقط یک هدف اصلی در داشبورد)
        if serializer.validated_data.get('is_active', True):
            FinancialGoal.objects.filter(user=self.request.user, is_active=True).update(is_active=False)
        serializer.save(user=self.request.user)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """جزئیات، ویرایش و حذف یک هدف."""
    serializer_class = FinancialGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)


class ActiveGoalProgressView(APIView):
    """
    پیشرفت هدف فعال (اصلی) کاربر - برای نمایش در داشبورد.
    اگر هدف فعالی وجود نداشته باشد 404 برمی‌گرداند.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        goal = FinancialGoal.objects.filter(user=request.user, is_active=True).first()
        if not goal:
            return Response({'detail': 'هدف فعالی ثبت نشده است.'}, status=status.HTTP_404_NOT_FOUND)

        progress = calculate_goal_progress(request.user, goal)

        if progress['is_achieved'] and not goal.is_achieved:
            goal.is_achieved = True
            goal.achieved_at = timezone.now()
            goal.save(update_fields=['is_achieved', 'achieved_at'])

        return Response(GoalProgressSerializer(progress).data)


class GoalProgressView(APIView):
    """پیشرفت یک هدف مشخص (با id)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        goal = get_object_or_404(FinancialGoal, pk=pk, user=request.user)
        progress = calculate_goal_progress(request.user, goal)
        return Response(GoalProgressSerializer(progress).data)
