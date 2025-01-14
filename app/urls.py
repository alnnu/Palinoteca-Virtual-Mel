
from django.urls import path

from app.views import create, createMulti, createScenario, getAllScenarios, getScenarioById, getImagesByScenario, updateScenarioById, deleteScenarioById, restoreScenarioById

urlpatterns = [
    path('/image/upload', create, name='upload'),
    path('/image/multi/upload', createMulti, name='create'),
    path('/image/scenario/create', createScenario, name='createScenario'),
    path('/image/scenario/all', getAllScenarios, name='getAllScenarios'),
    path('/image/scenario/<id>', getScenarioById, name='getScenarioById'),
    path('/image/scenario/<scenario_id>/images', getImagesByScenario, name='getImagesByScenario'),
    path('/image/scenario/update/<id>', updateScenarioById, name='updateScenarioById'),
    path('/image/scenario/delete/<id>', deleteScenarioById, name='deleteScenarioById'),
    path('/image/scenario/restore/<id>', restoreScenarioById, name='restoreScenarioById'),
]
