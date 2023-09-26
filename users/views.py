from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Определяем право доступа для редактирования профиля



