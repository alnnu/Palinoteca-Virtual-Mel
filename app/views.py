from http.client import responses

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response

from .ImageSerializer import ImageSerializer

@parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
def create(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=201)
    else:
        return Response(data=serializer.errors, status=400)
