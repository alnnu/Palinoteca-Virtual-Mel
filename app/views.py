from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .ImageSerializer import ImageSerializer, MultiImageSerializer, ScenarioSerializer

from .models import Scenario, Images

@swagger_auto_schema(
    methods=["post"],
    operation_description="upload one images",
    request_body=ImageSerializer,
    responses={400: 'bad request', 201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.FORMAT_UUID),
            'image': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(type=openapi.FORMAT_UUID),
            'scenario': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )}
)
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


@swagger_auto_schema(
    methods=["post"],
    operation_description="upload multiple images",
    manual_parameters=[
        openapi.Parameter('multiImages', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Images to upload"),
        openapi.Parameter('user', openapi.IN_FORM, type=openapi.FORMAT_UUID, description="User id"),
    ],
    responses={400: 'bad request', 201: openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.FORMAT_UUID),
                'image': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )}
)
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


@swagger_auto_schema(
    methods=["post"],
    operation_description="create a scenario",
    request_body=ScenarioSerializer,

    responses={400: 'bad request', 201: ScenarioSerializer}
)
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


@swagger_auto_schema(
    methods=["get"],
    operation_description="get all scenario",

    responses={404: 'not found', 200: openapi.Schema(
        type= openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "next": openapi.Schema(type=openapi.FORMAT_URI),
            "previous": openapi.Schema(type=openapi.FORMAT_URI),
            "results": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.FORMAT_UUID),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                        "plant": openapi.Schema(type=openapi.TYPE_STRING),
                        "isDeleted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        "user": openapi.Schema(type=openapi.FORMAT_UUID),
                    }
                )
            )
        }
    )}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllScenarios(request):
    paginator = PageNumberPagination()

    scenarios = Scenario.objects.all()

    paginated_notes = paginator.paginate_queryset(scenarios, request)

    serializer = ScenarioSerializer(paginated_notes, many=True)


    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    methods=["get"],
    operation_description="get one scenario",

    responses={404: 'not found', 200: ScenarioSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getScenarioById(request, id):
    scenario = Scenario.objects.filter(id=id).first()

    if scenario is not None:
        serializer = ScenarioSerializer(scenario)
        return Response(data=serializer.data, status=200)
    else:
        return Response(status=404)


@swagger_auto_schema(
    methods=["get"],
    operation_description="get all images in a scenario",

    responses={404: 'not found', 200: openapi.Schema(
        type= openapi.TYPE_OBJECT,
        properties={
            "count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "next": openapi.Schema(type=openapi.FORMAT_URI),
            "previous": openapi.Schema(type=openapi.FORMAT_URI),
            "results": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.FORMAT_UUID),
                        "image": openapi.Schema(type=openapi.TYPE_STRING),
                        "user": openapi.Schema(type=openapi.FORMAT_UUID),
                        "scenario": openapi.Schema(type=openapi.FORMAT_UUID),
                    }
                )
            )
        }
    )}
)
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

@swagger_auto_schema(
    methods=["put"],
    operation_description="uptade a scenario",
    request_body=ScenarioSerializer,
    responses={404: 'not found', 400: "bad request", 200: ScenarioSerializer}
)
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

@swagger_auto_schema(
    methods=["delete"],
    operation_description='delete one scenario',
    responses={404: 'not found', 200: openapi.Schema(
        type= openapi.TYPE_OBJECT,
        properties={
            'msg': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )}
)
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


@swagger_auto_schema(
    methods=["put"],
    operation_description='restore one scenario',
    responses={404: 'not found', 200: ScenarioSerializer}
)
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