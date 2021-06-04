from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                or request.method == 'POST'):
            return True
        return request.method in permissions.SAFE_METHODS
