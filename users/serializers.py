
from rest_framework import serializers

from learning.serializers import PaymentSerializer
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "payments"]

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "email"]
