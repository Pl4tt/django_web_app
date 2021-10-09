from django.db import models
from django.conf import settings

# ctrl + K then ctrl + C to comment, ctrl + K then ctrl + U to uncomment

class Message(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="sender", related_name="Messages", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
