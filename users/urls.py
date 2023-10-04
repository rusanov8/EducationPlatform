from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserUpdateView, UserCreateApiView, UserListApiView, UserDestroyAPIView, \
    UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/create', UserCreateApiView.as_view(), name='user-create'),
    path('users/', UserListApiView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete')
]
