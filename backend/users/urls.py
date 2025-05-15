from rest_framework.routers import DefaultRouter
from .views import UserViewSet,SubscriptionViewSet

router = DefaultRouter()
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("users", UserViewSet, basename="user")  # Измените URL-префикс

urlpatterns = router.urls