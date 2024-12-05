
from django.urls import path

from app.views import create, createMulti, createScenario, getAllScenarios, getScenarioById, updateScenarioById, deleteScenarioById

urlpatterns = [
    path('/image/upload', create, name='upload'),
    path('/image/multi/upload', createMulti, name='create'),
    path('/image/scenario/create', createScenario, name='createScenario'),
    path('/image/scenario/all', getAllScenarios, name='getAllScenarios'),
    path('/image/scenario/<id>', getScenarioById, name='getScenarioById'),
    path('/image/scenario/update/<id>', updateScenarioById, name='updateScenarioById'),
    path('/image/scenario/delete/<id>', deleteScenarioById, name='deleteScenarioById'),
]
