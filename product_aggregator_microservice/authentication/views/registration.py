from authentication.serializers.registration import RegistrationSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RegistrationView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return self.register(request)

    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response = {}
            user = serializer.save()
            response["message"] = "User successfully created!"
            response["username"] = user.username
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
