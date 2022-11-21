import base64
import io
import os
from random import randint
from zipfile import ZipFile

import requests
from django.core.files import File
from django.db.models.aggregates import Count
from django.http import HttpResponse
from PIL import Image, ImageOps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

from dog_api.models import Dog
from dog_api.serializer import DogSerializer


@api_view(['POST'])
def populate(request):
    # Populates the database with 12 dog pictures
    res = requests.get('https://dog.ceo/api/breeds/image/random/12')
    for dog in res.json()['message']:
        serializer = DogSerializer(data={"dog_image": dog})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'message': 'Dogs were successfully added to the database'}, HTTP_201_CREATED)

@api_view(['GET'])
def dog_list(request):
    return Response(DogSerializer(Dog.objects.all(), many=True).data, status=HTTP_200_OK)

@api_view(["DELETE"])
def dog_delete(request, dog_id):
    try:
        dog = Dog.objects.get(pk=dog_id)
        dog.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    except Dog.DoesNotExist:
        return Response({'message':f'{dog_id} does not exist'},status=HTTP_404_NOT_FOUND)

def get_image_from_url(dog_image):
    image_url = dog_image
    image_response = requests.get(image_url)
    image_data = image_response.content
    return image_data

@api_view(['GET'])
def dog_show(request):
    # we get a random dog from the database
    count = Dog.objects.all().count()
    random_index = randint(0, count-1)
    dog = DogSerializer(Dog.objects.all()[random_index]).data
    response = get_dog_image_pair(dog)
    return response

@api_view(['GET'])
def dog_image_pair_by_id(request, dog_id):
    dog = DogSerializer(Dog.objects.get(pk=dog_id)).data
    response = get_dog_image_pair(dog)
    return response

def get_dog_image_pair(dog):
    # we grab that dogs image bytes
    dog_image = dog['dog_image']
    dog_image = get_image_from_url(dog_image)

    # we flip the image
    uuid = dog["uuid"]
    original_image = Image.open(io.BytesIO(dog_image))
    flipped_image = ImageOps.flip(original_image)

    # we write both images to the disk
    original_image.save(f'{uuid}.jpg')
    flipped_image.save(f'{uuid}_flipped.jpg')

    # we zip both the images together
    zip_file = ZipFile(f'{uuid}.zip', mode='w')
    zip_file.write(f'{uuid}.jpg')
    zip_file.write(f'{uuid}_flipped.jpg')
    zip_file.close()

    # we send the zip file to the client
    zip_file = open(f'{uuid}.zip', mode='rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={dog["uuid"]}.zip'

    # we close and remove the files that are no longer needed
    zip_file.close()
    os.remove(f'{uuid}.zip')
    os.remove(f'{uuid}.jpg')
    os.remove(f'{uuid}_flipped.jpg')
    return response
