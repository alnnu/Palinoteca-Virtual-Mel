from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.UserSerilizer import UserSerializer

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
        return JsonResponse({'token': str(token), 'refreshToken': str(refresh)}, status=200)


