from django.db import models


class SingleMessage(models.Model):

    sender = models.CharField( max_length=255)
    receiver = models.CharField( max_length=255)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} message to {self.receiver}"
