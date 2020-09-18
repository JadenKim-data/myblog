from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        elif request.method == 'POST':
            return True
        else:
            return request.user and request.user.is_authenticated and obj.pk == request.user.pk

