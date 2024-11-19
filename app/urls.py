
from django.urls import path

from app.views import create, createMulti

urlpatterns = [
    path('/image/upload', create, name='upload'),
    path('/image/multi/upload', createMulti, name='create'),
]
