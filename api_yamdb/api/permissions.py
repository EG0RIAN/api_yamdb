from rest_framework import permissions, BasePermission

from users.models import User


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
        return request.user.role == User.admin


class ModeratorAuthorAdminSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)
