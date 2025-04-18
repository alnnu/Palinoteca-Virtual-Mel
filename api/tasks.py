from IA.inferencia import inferencia
from api.celery import app

@app.task()
def alanise(file):
   return inferencia(file)



