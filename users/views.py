
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.permissions import UserPermission
from users.serializers import UserSerializer, UserShortSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserShortSerializer
    permission_classes = [UserPermission]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        if str(request.user.pk) != pk:
            serializer = UserShortSerializer(user)
        return Response(serializer.data)
