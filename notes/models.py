import uuid
from accounts.models import User
from django.db import models


class Note(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=1000)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title 

    class Meta:
        ordering = ['-created_at']