from django.urls import path
from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView, UserCreateApiView, UserListApiView, UserDestroyAPIView, \
    UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('users/create', UserCreateApiView.as_view(), name='user-create'),
    path('users/', UserListApiView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('users/update/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete')
]
