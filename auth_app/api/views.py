from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)
