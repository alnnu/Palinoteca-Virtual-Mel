from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import Create, Login, CreateResetPasswordToken, ValidResetPasswordToken

urlpatterns = [
    path('/create', Create, name='Create User'),
    path('/login', Login, name='Login User'),
    path("/refresh", TokenRefreshView.as_view(), name='Refresh User'),
    path("/resetPassword/Create", CreateResetPasswordToken, name='Create Reset Password Token'),
    path("/resetPassword/<tokenId>", ValidResetPasswordToken, name='Reset Password Token'),
]