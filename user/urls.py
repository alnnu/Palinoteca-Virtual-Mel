from django.urls import path
from user.views import Create

urlpatterns = [
    path('/create', Create, name='Create User'),
]