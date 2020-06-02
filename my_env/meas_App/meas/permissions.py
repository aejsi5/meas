from rest_framework import permissions

class BelongsToClient(permissions.BasePermission):
    message= "You are only authorized to view objects of your client"

    """
    Object-level permission to only see objects of the authenticated users client
    """

    def has_object_permission(self, request, view, obj):
        if obj.Mandant == request.user.Mandant:
            return True
        else:
            return False
            
