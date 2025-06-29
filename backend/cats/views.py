"""View functions and classes for handling web requests in kittygram."""

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat
from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    """API for managing cats, auto-assigns owner on creation."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Assign current user as owner before saving Cat."""
        serializer.save(owner=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    """API endpoint for achievements, fetched without pagination."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None
