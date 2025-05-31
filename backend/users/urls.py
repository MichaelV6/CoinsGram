from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")  
router.register("", SubscriptionViewSet, basename="subscription")

urlpatterns = router.urls