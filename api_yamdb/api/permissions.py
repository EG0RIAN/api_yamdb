from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AnonimReadOnlyPermission(permissions.BasePermission):
    message = 'Разрешает анонимному пользователю только безопасные запросы.'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorAdminSuperuserOrReadOnlyPermission(permissions.BasePermission):
    message = (
        'Проверка пользователя является ли он администрацией'
        'или автором объекта иначе только safe запросы'
    )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )
