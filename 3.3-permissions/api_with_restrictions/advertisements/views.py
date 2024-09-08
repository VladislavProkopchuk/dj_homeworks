from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnly, IsAdmin
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["creator", ]  # filterset_class создает filterset_fields

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", ]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = (IsOwnerOrReadOnly | IsAdmin, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # draftless
        queryset = Advertisement.objects.all().exclude(status="DRAFT")
        user = self.request.user
        if user and user.is_authenticated:
            queryset_user = Advertisement.objects.filter(creator=user)
            queryset |= queryset_user
        return queryset


class FavoriteAdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # queryset = FavoriteAdvertisement.objects.all()
    serializer_class = FavoriteAdvertisementSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        permission_classes = [IsAuthenticated | IsAdminUser, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = FavoriteAdvertisement.objects.filter(subscriber=user)
        return queryset
