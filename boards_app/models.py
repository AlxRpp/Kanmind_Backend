from django.db import models
from django.contrib.auth.models import User


class Boards(models.Model):
    title = models.CharField(max_length=255, blank=False)
    members = models.ManyToManyField(User, related_name="member_boards")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_boards")

    def __str__(self):
        return f"BoardTitle: {self.title}, Owner: {self.owner}"

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ["id"]
