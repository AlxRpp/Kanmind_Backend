from django.urls import path
from .views import BoardView, SingleBoardView, EmailCheckView

urlpatterns = [
    path('boards/', BoardView.as_view(), name='boards'),
    path('boards/<int:pk>/', SingleBoardView.as_view(), name='single-board'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),



]
