
from django.urls import path

from app.views import create

urlpatterns = [
    path('image/upload', create, name='upload'),
]
