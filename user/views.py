from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
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