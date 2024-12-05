import uuid

from django.contrib.postgres.fields.array import ArrayField
from django.db import models

from user.models import User


def upload_to(instance, filename):
    return '/'.join(['images', str(instance.user.id), filename])


class Scenario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=False, blank=False)

    description = models.TextField(unique=True)

    objects = models.Manager()


class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    scenario = models.ForeignKey(Scenario, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    objects = models.Manager()





