
from rest_framework import serializers

from dogs.models import Breed, Dog, Ancestor

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["name", "description"]

class DogSerializer(serializers.ModelSerializer):
    breed_count = serializers.SerializerMethodField()
    breed = BreedSerializer()
    class Meta:
        model = Dog
        fields = ["id", "name", "breed", "breed_count", "breed"]

    def get_breed_count(self, instance):
        return Dog.objects.filter(breed=instance.breed).count()

class DogRetrieveSerializer(serializers.ModelSerializer):
    breed_count = serializers.SerializerMethodField()
    # breed = BreedSerializer()
    class Meta:
        model = Dog
        fields = ["id", "name", "breed", "breed_count", "breed"]

    def get_breed_count(self, instance):
        return Dog.objects.filter(breed=instance.breed).count()

class BreedRetrieveSerializer(serializers.ModelSerializer):
    dogs = DogRetrieveSerializer(many=True)
    class Meta:
        model = Breed
        fields = ["name", "description", "dogs"]

class AncestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ancestor
        fields = '__all__'