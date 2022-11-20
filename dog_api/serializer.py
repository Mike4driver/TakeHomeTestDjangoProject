import base64

import requests
from rest_framework import serializers

from dog_api.models import Dog


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = "__all__"
