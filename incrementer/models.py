from django.db import models

# Create your models here.
class KeyValue(models.Model):
    key = models.CharField(max_length=255 , primary_key=True, unique=True)
    value = models.IntegerField(default=0)