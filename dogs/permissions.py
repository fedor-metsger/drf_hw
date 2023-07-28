
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if view.get_object().published:
            return True
        return request.user == view.get_object().owner

class IsOwnerOrModerator(BasePermission):
    def has_permission(self, request, view):
        if view.get_object().published:
            return True
        return request.user == view.get_object().owner or "moderator" in [i.name for i in request.user.groups.all()]
