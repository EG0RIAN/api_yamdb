from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class AnonimReadOnlyPermission(permissions.BasePermission):
    message = 'Разрешает анонимному пользователю только безопасные запросы.'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


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


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    message = (
        'Проверка на запросы, только от администрации.'
    )

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin)
        )