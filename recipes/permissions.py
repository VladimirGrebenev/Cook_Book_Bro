from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsCook(BasePermission):
    message = "You are not the Cook!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.cook:
            return True
        return False


class IsChef(BasePermission):
    message = "You are not a Chef!"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.CHEF:
            return True
        return False
