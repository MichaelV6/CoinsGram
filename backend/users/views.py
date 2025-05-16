
from rest_framework import viewsets, permissions, mixins
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiTypes, extend_schema_view, OpenApiResponse, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SubscriptionSerializer, SetPasswordSerializer
from .models import Subscription
from api.exceptions import PermissionDeniedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
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
        request=SetPasswordSerializer,
        responses={
          204: OpenApiTypes.NONE,
          400: OpenApiResponse(description="Ошибка валидации")
        },
        description="Смена пароля текущего пользователя"
    )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='set_password')
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)    


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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="subscribed_to",
                description="ID пользователя, от которого нужно отписаться",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={204: OpenApiTypes.NONE, 404: OpenApiResponse(description="Подписка не найдена")},
        description="Удалить подписку по ID пользователя (subscribed_to) через query-параметр",
        methods=["DELETE"]
    )
    @action(detail=False, methods=['delete'], url_path='by_user')
    def delete_by_user(self, request):
        subscribed_to_id = request.query_params.get('subscribed_to')
        if not subscribed_to_id:
            return Response(
                {'detail': 'subscribed_to обязателен как query param'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance = Subscription.objects.filter(
            user=request.user,
            subscribed_to_id=subscribed_to_id
        ).first()
        if not instance:
            return Response({'detail': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
