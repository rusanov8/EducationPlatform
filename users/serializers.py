from rest_framework import serializers

from education.serializers import CourseSerializer
from payments.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True, read_only=True, source='payments.all')

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):  # Для создания пользователя
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city')


class UserUpdateProfileSerializer(serializers.ModelSerializer):  # Для редактирования своего профиля
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'password')


class SelfProfileSerializer(serializers.ModelSerializer):  # Для просмотра своего профиля

    courses = CourseSerializer(many=True)
    payments = PaymentSerializer(many=True, read_only=True, source='payments.all')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'courses', 'payments')


class OtherProfilesSerializer(serializers.ModelSerializer):  # Для просмотра чужих профилей

    courses = CourseSerializer(many=True)
    class Meta:
        model = User
        fields = ('first_name', 'phone', 'city', 'avatar', 'courses')
