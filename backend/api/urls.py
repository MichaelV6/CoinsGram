from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CoinViewSet, FavoriteViewSet
from users.views import UserViewSet, SubscriptionViewSet
from comments.views import CommentViewSet
router = DefaultRouter()
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('comments', CommentViewSet, basename='comment')
router.register('tags', TagViewSet, basename='tag')
router.register('coins', CoinViewSet, basename='coin')
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]