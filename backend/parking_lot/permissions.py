from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a super user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS and request.user and request.user.is_authenticated) or
            (request.user and request.user.is_superuser)
        )
