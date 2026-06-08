from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import BoardSerializer
from ..models import Boards
from django.db.models import Q


class BoardView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        query = Boards.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)).distinct()
        return query
