from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from incrementer.models import KeyValue
from incrementer.serializer import KeyValueSerializer


@api_view(['GET'])
def key_list(request):
    return Response(KeyValueSerializer(KeyValue.objects.all(), many=True).data, status=HTTP_200_OK)
    

@api_view(['POST'])
def key_create(request):
    serializer = KeyValueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def key(request, key):
    try:
        key_data = KeyValue.objects.get(pk=key)

        if request.method == 'GET':
            serializer = KeyValueSerializer(key_data)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = KeyValueSerializer(key_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            key_data.delete()
            return Response(status=HTTP_204_NO_CONTENT)

    except KeyValue.DoesNotExist:
        return Response({'message':'Key does not exist'},status=HTTP_404_NOT_FOUND)
@api_view(['PUT'])
def key_inc(request, key):
    try:
        data = KeyValue.objects.get(pk=key)
        data.value = F('value') + 1
        data.save()
        return Response(status=HTTP_204_NO_CONTENT)
    except KeyValue.DoesNotExist:
        return Response({'message':f'{key} does not exist'},status=HTTP_404_NOT_FOUND)
