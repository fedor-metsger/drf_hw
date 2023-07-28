
from django.db.models import Q

from rest_framework import generics, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from dogs.models import Breed, Dog, Ancestor
from dogs.permissions import IsOwner, IsOwnerOrModerator
from dogs.serializers import BreedSerializer, DogSerializer, AncestorSerializer, BreedRetrieveSerializer
from dogs.paginators import DogPaginator


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class BreedListAPIView(generics.ListAPIView):
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()

class BreedRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BreedRetrieveSerializer
    queryset = Breed.objects.all()

class DogListAPIView(generics.ListAPIView):
    serializer_class = DogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DogPaginator

    def get_queryset(self):
        if "moderator" in [i.name for i in self.request.user.groups.all()]:
            return Dog.objects.all()
        else:
            return Dog.objects.filter(Q(owner=self.request.user) | Q(published=True))

class DogRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()
    permission_classes = [IsOwnerOrModerator]

class DogCreateAPIView(CreateAPIView):
    serializer_class = DogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_dog = serializer.save()
        new_dog.owner = self.request.user
        new_dog.save()

class AncestorViewSet(viewsets.ModelViewSet):
    queryset = Ancestor.objects.all()
    serializer_class = AncestorSerializer
