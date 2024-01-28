from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTime(auto_now_add=True)
