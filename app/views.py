from http.client import responses

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .ImageSerializer import ImageSerializer, MultiImageSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(data=serializer.data, status=201)
    else:
        return Response(data=serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def createMulti(request):
    serializer = MultiImageSerializer(data=request.data)

    if serializer.is_valid():
        res =  serializer.create(request.data)
        print(serializer)
        return Response(data=res, status=201)
    else:
        return Response(data=serializer.errors, status=400)