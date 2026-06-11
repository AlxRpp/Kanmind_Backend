from django.urls import path
from .views import PostTaskView, UpdateAndDeleteTaskView

urlpatterns = [
    path('tasks/', PostTaskView.as_view(), name='post_task'),
    path('tasks/<int:pk>/', UpdateAndDeleteTaskView.as_view(), name='task_detail'),

]
