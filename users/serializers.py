from rest_framework import serializers

from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city')


class UserProfileSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True, read_only=True, source='payments.all')
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city', 'payments')
