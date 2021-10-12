from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model



class PrivateChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="owner", related_name="owning_chats", on_delete=models.CASCADE, null=True)
    administrators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="private_admin_chats")
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="private_chats", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_name}"
    
    def check_user(self, user: settings.AUTH_USER_MODEL) -> bool:
        """
        Returns True if the given user is in the allowed users else false.
        """
        return user in self.allowed_users.all()
    
    def check_admin(self, user: settings.AUTH_USER_MODEL) -> bool:
        """
        Returns True if the given user is in an admin of this chat else false.
        """
        return user in self.administrators.all()
    
    def add_user(self, user: settings.AUTH_USER_MODEL):
        """
        Adds the given user to the allowed users if not already.
        """
        if not self.check_user(user):
            self.allowed_users.add(user)

        self.save()

    def add_users(self, users: list[settings.AUTH_USER_MODEL]):
        """
        Adds all given users to the allowed users if not already.
        """
        for user in users:
            self.add_user(user)

        self.save()

    def remove_user(self, user: settings.AUTH_USER_MODEL):
        """
        Removes the given user from the allowed users if exist.
        """
        if self.check_user(user):
            self.allowed_users.remove(user)
        
    def add_administrator(self, user: settings.AUTH_USER_MODEL):
        """
        Adds the given user to the administrators and the allowed users if not already.
        """
        if not self.check_user(user):
            self.add_user(user)
        
        if not self.check_admin(user):
            self.administrators.add(user)
        
        self.save()

    def remove_administrator(self, user: settings.AUTH_USER_MODEL):
        """
        Removes the given user from the administrators if exist.
        """
        if self.check_admin(user):
            self.administrators.remove(user)
        
        self.save()


class PrivateMessage(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="sender", related_name="private_messages", on_delete=models.CASCADE)
    chat_room = models.ForeignKey(PrivateChatRoom, related_name="messages", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class PublicMessage(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="sender", related_name="messages", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
