
from rest_framework import serializers


class DogNameValidator():

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        name = dict(value).get(self.field)
        if name.lower() in ["продам", "крипта", "ставки"]:
            raise serializers.ValidationError("Нельзя размещать коммерческие объявления.")
