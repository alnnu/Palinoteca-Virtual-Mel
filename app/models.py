import uuid

from django.db import models

def upload_to(instance, filename):
    return '/'.join(['images', str(instance.id), filename])

class Images(models.Model):
    image = models.ImageField(upload_to=upload_to)


