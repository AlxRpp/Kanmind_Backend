from django.db import models
from django.contrib.auth.models import User
from boards_app.models import Boards


class Tasks(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To DO'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    board = models.ForeignKey(
        Boards, on_delete=models.CASCADE, related_name='task')
    title = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=250, blank=True)
    status = models.CharField(
        max_length=250, choices=STATUS_CHOICES, blank=False)
    priority = models.CharField(
        max_length=250, choices=PRIORITY_CHOICES, blank=False)
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignee')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewer')
    due_date = models.DateField()
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Board: {self.board}, Title: {self.title} "

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['id']
