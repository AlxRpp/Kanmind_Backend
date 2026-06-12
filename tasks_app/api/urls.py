from django.urls import path
from .views import PostTaskView, UpdateAndDeleteTaskView, AssignedToMeView, ReviewingView, CommentsView, DeleteComment

urlpatterns = [
    path('tasks/', PostTaskView.as_view(), name='post_task'),
    path('tasks/<int:pk>/', UpdateAndDeleteTaskView.as_view(), name='task_detail'),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned_to_me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewing'),
    path('tasks/<int:pk>/comments/', CommentsView.as_view(), name='comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/',
         DeleteComment.as_view(), name='delete_comment')

]
