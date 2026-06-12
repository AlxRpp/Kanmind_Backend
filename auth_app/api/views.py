from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegistrationView(APIView):
    permission_classes = [AllowAny]

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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = {}
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': 'Email and Password required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            pw_check = user.check_password(password)

            if pw_check:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                    'fullname': user.username,
                    'email': user.email,
                    'user_id': user.id
                }
            else:
                return Response({'error': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)
