
from rest_framework import generics, viewsets
from rest_framework.generics import CreateAPIView

from dogs.models import Breed, Dog, Ancestor
from dogs.serializers import BreedSerializer, DogSerializer, AncestorSerializer, BreedRetrieveSerializer


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
    queryset = Dog.objects.all()

class DogRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()

class DogCreateAPIView(CreateAPIView):
    serializer_class = DogSerializer

class AncestorViewSet(viewsets.ModelViewSet):
    queryset = Ancestor.objects.all()
    serializer_class = AncestorSerializer