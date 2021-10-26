from rest_framework import permissions

#create custom permission for annonomous user

class AnonPermissionOnly(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = "You are alreay authenticated. logout please"
    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        return not request.user.is_authenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
