
from rest_framework import serializers

from dogs.models import Breed, Dog, Ancestor

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = '__all__'

class AncestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ancestor
        fields = '__all__'