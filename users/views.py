from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserCreateSerializer, UserUpdateProfileSerializer, SelfProfileSerializer, \
    OtherProfilesSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = OtherProfilesSerializer
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return SelfProfileSerializer
        else:
            return OtherProfilesSerializer


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]



