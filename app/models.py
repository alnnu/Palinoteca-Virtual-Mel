import uuid

from django.db import models

from user.models import User


def upload_to(instance, filename):
    return '/'.join(['images', str(instance.id), filename])

class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    objects = models.Manager()


