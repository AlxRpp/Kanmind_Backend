from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import PostTaskSerializer, UpdateAndDeleteTaskSerializer
from django.shortcuts import get_object_or_404
from ..models import Tasks
from boards_app.models import Boards


class PostTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostTaskSerializer

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Boards, pk=request.data.get('board'))
        if request.user != obj.owner and request.user not in obj.members.all():
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UpdateAndDeleteTaskView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateAndDeleteTaskSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Tasks, pk=pk)
        if obj.board.owner != self.request.user and self.request.user not in obj.board.members.all():
            raise PermissionDenied
        return obj

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Tasks, pk=self.kwargs['pk'])
        if obj.creator != self.request.user and request.user != obj.board.owner:
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)
