from django.db import models
from django.conf import settings

class Message(models.Model):
    message_text = models.CharField(max_length=512)
    message_date = models.DateTimeField()
    message_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )