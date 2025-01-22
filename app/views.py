from http.client import responses

from django.core.paginator import Paginator
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .Serializers import ImageSerializer, MultiImageSerializer, ScenarioSerializer

from .models import Scenario, Images

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

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

        return Response(data=res, status=201)
    else:
        return Response(data=serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createScenario(request):
    serializer = ScenarioSerializer(data=request.data)

    if serializer.is_valid():
        scenario = Scenario.objects.filter(description=request.data['description']).first()

        if scenario is None:
            serializer.save()
            return  Response(data=serializer.data, status=201)
    else:
        return Response(data=serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllScenarios(request):
    paginator = PageNumberPagination()

    scenarios = Scenario.objects.all()

    paginated_notes = paginator.paginate_queryset(scenarios, request)

    serializer = ScenarioSerializer(paginated_notes, many=True)


    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getScenarioById(request, id):
    scenario = Scenario.objects.filter(id=id).first()

    if scenario is not None:
        serializer = ScenarioSerializer(scenario)
        return Response(data=serializer.data, status=200)
    else:
        return Response(status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getImagesByScenario(request, scenario_id):

    paginator = PageNumberPagination()

    scenario = Scenario.objects.filter(id=scenario_id).first()

    if scenario is not None:
        images = Images.objects.all().filter(scenario=scenario)

        paginated_notes = paginator.paginate_queryset(images, request)

        serializer = ImageSerializer(paginated_notes, many=True)


        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(status=404)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateScenarioById(request, id):
    scenario = Scenario.objects.filter(id=id).first()

    if scenario is not None:
        serializer = ScenarioSerializer(scenario, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        else:
            return Response(data=serializer.errors, status=400)
    else:
        return Response(status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteScenarioById(request, id):
    scenario = Scenario.objects.filter(id=id, isDeleted = False).first()
    if scenario is not None:
        scenario.isDeleted = True
        scenario.save()
        return Response(data={"msg": "Scenario object deleted"},status=200)
    else:
        return Response(status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def restoreScenarioById(request, id):
    scenario = Scenario.objects.filter(id=id).first()

    if scenario is not None:
        scenario.isDeleted = False
        scenario.save()
        serializer = ScenarioSerializer(scenario)
        return Response(data=serializer.data,status=200)
    else:
        return Response(status=404)


