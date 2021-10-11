from django.db import models
from django.conf import settings


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="friend_list", on_delete=models.CASCADE)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username
    
    def add_friend(self, friend: settings.AUTH_USER_MODEL):
        """
        Adds the friend to the selfs friends list.
        """
        if not friend in self.friends.all():
            self.friends.add(friend)

            self.save()
        
    def remove_friend(self, friend: settings.AUTH_USER_MODEL):
        """
        Removes the friend from the selfs friends list.
        """
        if friend in self.friends.all():
            self.friends.remove(friend)

            self.save()

    def friend(self, friend: settings.AUTH_USER_MODEL):
        """
        Sets the friend on the selfs friends list and the selfs user on the friends friend list.
        """
        friends_list = FriendList.objects.get(user=friend)

        self.add_friend(friend)
        friends_list.add_friend(self.user)

    def unfriend(self, friend: settings.AUTH_USER_MODEL):
        """
        Removes the friend from the selfs friends list and the selfs user on the friends friend list.
        """
        friends_list = FriendList.objects.get(user=friend)

        self.remove_friend(friend)
        friends_list.remove_friend(self.user)
    


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friends_requested", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friend_requests", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sender.username} requested {self.receiver.username}"
    
    def accept(self):
        """
        Executes when the receiver accepts the friend request, friends the receiver with the sender, sets is_active to false.
        """
        if self.is_active:
            friend_list = FriendList.objects.get(user=self.receiver)
            friend_list.friend(self.sender)

            self.is_active = False

            self.save()

    def reactivate(self):
        """
        Executes when the sender sends a friend request to the receiver again, sets is_active to true.
        """
        self.is_active = True

        self.save()

    def decline(self):
        """
        Executes when the receiver declines the friend request, sets is_active to false.
        """
        self.is_active = False

        self.save()

    def cancel(self):
        """
        Executes when the sender canceles the friend request, sets is_active to false.
        """
        self.is_active = False
        
        self.save()


