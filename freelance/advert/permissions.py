from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.customer == request.user


class IsCustomer(permissions.BasePermission):
    """
    Permission to only allow user_type 'Customer' to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.user_type == "Customer"


class IsExecutor(permissions.BasePermission):
    """
    Permission to only allow user_type 'Executor' to edit it.
    """

    def has_permission(self, request, view):
        return request.user.user_type == "Executor"
