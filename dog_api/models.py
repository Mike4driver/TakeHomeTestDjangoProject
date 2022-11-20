import uuid

from django.db import models


# Create your models here.
class Dog(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    dog_image = models.CharField(max_length=255)
