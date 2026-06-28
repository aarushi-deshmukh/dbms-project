from rest_framework import permissions

class IsBuyer(permissions.BasePermission):
    """
    Allows access only to users who have an associated Buyer profile.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'buyer')
        )


class IsSeller(permissions.BasePermission):
    """
    Allows access only to users who have an associated Seller profile.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'seller')
        )
