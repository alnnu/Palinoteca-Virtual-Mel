from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.UserSerilizer import UserSerializer

@api_view(['post'])
def Create(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)