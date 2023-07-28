
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().owner

class IsOwnerOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().owner or "moderator" in [i.name for i in request.user.groups.all()]

class NotModerator(BasePermission):
    def has_permission(self, request, view):
        return not "moderator" in [i.name for i in request.user.groups.all()]


from rest_framework import permissions


class LessonPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return request.user.is_authenticated
        elif view.action in ["create", "destroy"]:
            if "moderator" in [i.name for i in request.user.groups.all()]:
                return False
            return request.user.is_authenticated
        elif view.action in ["retrieve", "update", "partial_update"]:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action == "retrieve":
            return obj.owner == request.user or "moderator" in [i.name for i in request.user.groups.all()]
        elif view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == request.user and not "moderator" in [i.name for i in request.user.groups.all()]
        else:
            return False
