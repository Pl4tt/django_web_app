from django.db import models
from django.conf import settings


class PublicChatRoom(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text="Users connected to the room.", blank=True, null=True)

    @property
    def room_group_name(self):
        return f"chat_{self.pk}"

class Message(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="sender", on_delete=models.CASCADE)
    chat = models.ForeignKey(PublicChatRoom, verbose_name="chat", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
