
from rest_framework import serializers

from dogs.models import Breed, Dog, Ancestor
from dogs.services import convert_currencies
from dogs.validators import DogNameValidator


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["name", "description"]

class DogSerializer(serializers.ModelSerializer):
    breed_count = serializers.SerializerMethodField()
    # breed = BreedSerializer()
    usd_price = serializers.SerializerMethodField()
    eur_price = serializers.SerializerMethodField()

    class Meta:
        model = Dog
        fields = ["id", "name", "owner", "breed", "breed_count", "price", "usd_price", "eur_price"]
        validators = [DogNameValidator(field="name")]

    def get_breed_count(self, instance):
        return Dog.objects.filter(breed=instance.breed).count()

    def get_usd_price(self, instance):
        return convert_currencies("USD", instance.price)

    def get_eur_price(self, instance):
        return convert_currencies("EUR", instance.price)

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
