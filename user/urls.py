from django.urls import path
from user.views import Create, Login

urlpatterns = [
    path('/create', Create, name='Create User'),
    path('/login', Login, name='Login User'),
]