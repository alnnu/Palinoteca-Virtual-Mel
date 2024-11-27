from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.UserSerilizer import UserSerializer, ResetPasswordTokenSerializerCreate, ResetPasswordTokenSerializer
from user.models import ResetPasswordToken


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


@api_view(['post'])
def ValidResetPasswordToken(request):

    serializer = ResetPasswordTokenSerializer(data=request.data)

    if serializer.is_valid():
        tokenId = request.query_parans.get('tokenId')

        token = ResetPasswordToken.objects.filter(id=tokenId).first()

        if serializer.isTokenValid(token):
            print(token.user)
            return JsonResponse({'token': token.id}, status=200)
    else:

        return JsonResponse(serializer.errors, status=400)