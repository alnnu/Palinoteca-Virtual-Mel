
from django.urls import path

from app.views import create

urlpatterns = [
    path('/upload', create, name='upload'),
]
