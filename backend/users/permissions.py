# backend/users/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Разрешает доступ владельцу объекта или администратору.
    """
    def has_object_permission(self, request, view, obj):
        # безопасные методы (GET, HEAD) пропускаем — их уже разрешает IsAuthenticatedOrReadOnly
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or obj.id == request.user.id
