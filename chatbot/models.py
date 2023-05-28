from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"ChatHistory: {self.user.username} - {self.prompt}"

