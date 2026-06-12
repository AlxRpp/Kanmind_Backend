from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.exceptions import PermissionDenied
from .serializers import BoardSerializer, GetSingleBoardSerializer, WriteAndDeleteSingleBoardSerializer, EmailCheckSerializer
from ..models import Boards
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class BoardView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    # Owner is taken from the token, not from request body.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Returns boards where the user is owner or member. distinct() prevents duplicates.
    def get_queryset(self):
        query = Boards.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)).distinct()
        return query


class SingleBoardView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GetSingleBoardSerializer
    permission_classes = [IsAuthenticated]

    # Returns the board if the user is owner or member, otherwise raises 403.
    def get_object(self):
        obj = get_object_or_404(Boards, pk=self.kwargs['pk'])
        if obj.owner != self.request.user and self.request.user not in obj.members.all():
            raise PermissionDenied
        return obj

    # Only the owner can delete the board, not just any member.
    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Boards, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)

    # GET returns nested read data, all other methods use the write serializer.
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetSingleBoardSerializer
        return WriteAndDeleteSingleBoardSerializer


class EmailCheckView(APIView):
    serializer = EmailCheckSerializer
    permission_classes = [IsAuthenticated]

    # Checks if a user with that email exists. Email is passed as query param, not in body.
    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            return Response({
                'id': user.id,
                'email': user.email,
                'fullname': user.username
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
