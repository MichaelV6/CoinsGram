from rest_framework import viewsets, permissions, decorators
from rest_framework.response import Response
from django.http import FileResponse
from docx import Document
from io import BytesIO
from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema
from coins.models import Coin
from tags.models import Tag
from users.models import User
from favorites.models import Favorite
from .serializers import (
    TagSerializer,
    CoinReadSerializer, CoinWriteSerializer, FavoriteSerializer)
from .filters import CoinFilter
from users.serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if self.request.method in permissions.SAFE_METHODS:
            # читать может любой
            return [permissions.AllowAny()]
        # создавать/редактировать/удалять — только админ
        return [permissions.IsAdminUser()]

# ----- Монеты -----
class CoinViewSet(viewsets.ModelViewSet):
    queryset = Coin.objects.select_related('author').prefetch_related('tags')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = CoinFilter
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ('name', 'description')
    ordering_fields = ('estimated_value', 'pub_date')

    @extend_schema(
        request={
            'multipart/form-data': CoinWriteSerializer
        },
        responses=CoinReadSerializer
    )
    def create(self, request, *args, **kwargs):
        # Исправляем для правильной обработки multipart/form-data
        if not request.FILES.get('image'):
            return Response(
                {'error': 'Изображение монеты обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ('POST', 'PUT', 'PATCH'):
            return CoinWriteSerializer
        return CoinReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def perform_update(self, serializer):
        # Проверяем, является ли пользователь автором или админом
        coin = self.get_object()
        if not self.request.user.is_staff and coin.author != self.request.user:
            raise PermissionDeniedError("Вы можете редактировать только свои монеты")
        serializer.save()
        
    def perform_destroy(self, instance):
        # Проверяем права на удаление
        if not self.request.user.is_staff and instance.author != self.request.user:
            raise PermissionDeniedError("Вы можете удалять только свои монеты")
        instance.delete()

# ----- Избранное -----
class FavoriteViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def list(self, request, *args, **kwargs):
        coins = Coin.objects.filter(in_favorites__user=request.user)
        serializer = CoinReadSerializer(coins, many=True)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=['get'])
    def download(self, request):
        coins = Coin.objects.filter(in_favorites__user=request.user)
        doc = Document()
        doc.add_heading('Список избранного', level=1)
        table = doc.add_table(rows=1, cols=5)
        hdr = table.rows[0].cells
        hdr[0].text = '№'
        hdr[1].text = 'Название'
        hdr[2].text = 'Теги'
        hdr[3].text = 'Цена, ₽'
        hdr[4].text = 'Продавец'
        for i, coin in enumerate(coins, start=1):
            cells = table.add_row().cells
            cells[0].text = str(i)
            cells[1].text = coin.name
            cells[2].text = ', '.join(t.name for t in coin.tags.all())
            cells[3].text = str(coin.estimated_value)
            cells[4].text = coin.author.username
        buf = BytesIO()
        doc.save(buf)
        buf.seek(0)
        return FileResponse(
            buf,
            as_attachment=True,
            filename='favorites.docx'
        )
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            # Любой может создать пользователя (регистрация)
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Только владелец аккаунта или админ может изменять/удалять
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        else:
            # Для просмотра списка пользователей нужна авторизация
            return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        # Проверяем права на обновление
        if not self.request.user.is_staff and self.request.user.id != self.kwargs.get('pk'):
            raise PermissionDeniedError("Вы можете редактировать только свой профиль")
        serializer.save()
        
    def perform_destroy(self, instance):
        # Проверяем права на удаление
        if not self.request.user.is_staff and self.request.user.id != instance.id:
            raise PermissionDeniedError("Вы можете удалять только свой профиль")
        instance.delete()

# Добавьте классы разрешений
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешение для проверки владельца ресурса или администратора
    """
    def has_object_permission(self, request, view, obj):
        # Администраторы могут делать всё
        if request.user.is_staff:
            return True
            
        # Проверяем является ли пользователь владельцем
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        # Для профиля пользователя
        elif isinstance(obj, User):
            return obj.id == request.user.id
        return False