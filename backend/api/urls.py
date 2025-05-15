from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CoinViewSet, FavoriteViewSet
from users.views import UserViewSet
router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('coins', CoinViewSet, basename='coin')
router.register('favorites', FavoriteViewSet, basename='favorite')
# Заменим UserViewSet из users.urls на наш UserViewSet с правильными правами доступа
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # Оставим только маршруты подписок из users.urls
    path('subscriptions/', include('users.urls')),
]