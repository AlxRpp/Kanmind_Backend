from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import PostTaskSerializer, UpdateAndDeleteTaskSerializer, AssignedToMeOrReviewerSerializer, CommentsSerializer
from django.shortcuts import get_object_or_404
from ..models import Tasks, Comments
from boards_app.models import Boards


class PostTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostTaskSerializer

    def post(self, request, *args, **kwargs):
        """Checks board membership before creating. Only members and the owner can add tasks."""
        obj = get_object_or_404(Boards, pk=request.data.get('board'))
        if request.user != obj.owner and request.user not in obj.members.all():
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Sets creator from the token, not the request body."""
        serializer.save(creator=self.request.user)


class UpdateAndDeleteTaskView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateAndDeleteTaskSerializer

    def get_object(self):
        """Only board members and the owner can access this task."""
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Tasks, pk=pk)
        if obj.board.owner != self.request.user and self.request.user not in obj.board.members.all():
            raise PermissionDenied
        return obj

    def destroy(self, request, *args, **kwargs):
        """Task creator or board owner can delete. Regular members can't."""
        obj = get_object_or_404(Tasks, pk=self.kwargs['pk'])
        if obj.creator != self.request.user and request.user != obj.board.owner:
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)


class AssignedToMeView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignedToMeOrReviewerSerializer

    def get_queryset(self):
        return Tasks.objects.filter(assignee=self.request.user)


class ReviewingView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignedToMeOrReviewerSerializer

    def get_queryset(self):
        return Tasks.objects.filter(reviewer=self.request.user)


class CommentsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializer

    def get_task(self):
        """Helper to fetch the task and check board membership in one place."""
        task = get_object_or_404(Tasks, pk=self.kwargs.get('pk'))
        if task.board.owner != self.request.user and self.request.user not in task.board.members.all():
            raise PermissionDenied
        return task

    def get_queryset(self):
        return Comments.objects.filter(task=self.get_task())

    def post(self, request, *args, **kwargs):
        self.get_task()
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, task=self.get_task())


class DeleteComment(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comments.objects.all()

    def get_object(self):
        """Fetches task and comment by their own IDs from the URL. Only the comment author can delete."""
        task = get_object_or_404(Tasks, pk=self.kwargs.get('task_id'))
        comment = get_object_or_404(Comments, pk=self.kwargs.get('comment_id'))
        if comment.author != self.request.user:
            raise PermissionDenied
        return comment
