
from rest_framework import viewsets, permissions, mixins
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiTypes, extend_schema_view

from .serializers import UserSerializer, SubscriptionSerializer
from .models import Subscription
from api.exceptions import PermissionDeniedError

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        responses=UserSerializer(many=True),
        description="Список всех пользователей (только для авторизованных)"
    ),
    retrieve=extend_schema(
        responses=UserSerializer,
        description="Профиль пользователя"
    ),
    destroy=extend_schema(
        responses={204: OpenApiTypes.NONE},
        description="Удаление своего профиля"
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Регистрация пользователя с возможностью загрузки аватара"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="Полное обновление профиля (PUT) с аватаром"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="Частичное обновление профиля (PATCH) с аватаром"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema_view(
    list=extend_schema(
        responses=SubscriptionSerializer(many=True),
        description="Список подписок текущего пользователя"
    ),
    create=extend_schema(
        request=SubscriptionSerializer,
        responses={201: SubscriptionSerializer},
        description="Подписаться на пользователя"
    ),
    destroy=extend_schema(
        responses={204: OpenApiTypes.NONE},
        description="Отписаться от пользователя"
    ),
)
class SubscriptionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDeniedError("Удалять можно лишь свои подписки")
        instance.delete()


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # профиль пользователя
        if isinstance(obj, User):
            return obj.id == request.user.id
        # подписка
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False