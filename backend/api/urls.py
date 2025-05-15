from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CoinViewSet, FavoriteViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('coins', CoinViewSet, basename='coin')
router.register('favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),  # <-- вот так!
]
