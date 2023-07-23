
from rest_framework import generics, viewsets
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer