from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)

from user.views import (
    RegisterAPIView,
    ParkingLotTokenObtainPairAPIView,
    UserProfileAPIView
)

app_name = 'user'

urlpatterns = [
    path('auth/register', RegisterAPIView.as_view(), name='register'),
    path('auth/login', ParkingLotTokenObtainPairAPIView.as_view(), name='login'),
    path('auth/verify', TokenVerifyView.as_view(), name='verify'),
    path('auth/refresh', TokenRefreshView.as_view(), name='refresh'),

    path('user/profile', UserProfileAPIView.as_view(), name='profile'),
]
