from drf_yasg import openapi
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from user.UserSerilizer import UserSerializer, ResetPasswordTokenSerializerCreate, ResetPasswordTokenSerializer
from user.models import ResetPasswordToken


@swagger_auto_schema(
    methods=['POST'],
    operation_description="create an user",
    responses={400: 'Bad Request', 201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.FORMAT_UUID),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email','passwordConfirm', 'password', 'name'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'passwordConfirm': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    )
@api_view(['post'])
def Create(request):
    password = request.data['password']
    confirm_password = request.data['passwordConfirm']

    if password != confirm_password:
        return JsonResponse({'password': ['Passwords do not match']}, status=400)


    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    methods=['POST'],
    operation_description="create an user",
    responses={400: 'Bad Request', 200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'access': openapi.Schema(type=openapi.TYPE_STRING),
            'refreshToken': openapi.Schema(type=openapi.TYPE_STRING),
            'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.FORMAT_UUID),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                        })
        }
    )},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    )
@api_view(['post'])
def Login(request):
    password = request.data['password']
    email = request.data['email']

    user = authenticate(email=email, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid email or password'}, status=400)
    else:

        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        userRes = UserSerializer(user)

        return JsonResponse({'access': str(token), 'refreshToken': str(refresh), 'user' : userRes.data}, status=200)



@swagger_auto_schema(
    methods=['POST'],
    operation_description="create an user",
    responses={400: 'Bad Request', 201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Token': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'userEmail': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    )
@api_view(['post'])
def CreateResetPasswordToken(request):

    serializer = ResetPasswordTokenSerializerCreate(data=request.data)

    if serializer.is_valid():
        token = serializer.create(request.data)

        if token is not None:
            return JsonResponse({"Token": token.id}, status=201)
        else:
            return JsonResponse({'error': 'User not Found'}, status=400)
    else:

        return JsonResponse(serializer.errors, status=400)


@swagger_auto_schema(
    methods=['POST'],
    operation_description="create an user",
    responses={400: 'Bad Request', 200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'msg': openapi.Schema(type=openapi.TYPE_STRING)
        }
    )},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['newPassword', 'newPasswordConfirm'],
        properties={
            'newPassword': openapi.Schema(type=openapi.TYPE_STRING),
            'newPasswordConfirm': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    )
@api_view(['post'])
def ValidResetPasswordToken(request, tokenId):

    password = request.data['newPassword']
    confirm_password = request.data['newPasswordConfirm']

    error = ""

    serializer = ResetPasswordTokenSerializer(data=request.data)

    if serializer.is_valid():

        token = ResetPasswordToken.objects.filter(id=tokenId).first()

        if serializer.isTokenValid(token):

            if password == confirm_password:
                serializer.changePassword(validated_data=request.data, user=token.user)

                token.delete()

                return JsonResponse({'msg': "password changed"}, status=200)
            else:
                error = "Password does not match"
        else:
            error = "Invalid token"


        return JsonResponse({'Error': error}, status=400)
    else:

        return JsonResponse(serializer.errors, status=400)