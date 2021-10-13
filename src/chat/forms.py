from django import forms
from django.contrib.auth import get_user_model

from .models import PrivateChatRoom

class ChatRoomCreationForm(forms.ModelForm):

    class Meta:
        model = PrivateChatRoom
        fields = ("room_name", "allowed_users")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ChatRoomCreationForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        chat_room = super(ChatRoomCreationForm, self).save(commit=False)
        chat_room.room_name = self.cleaned_data["room_name"]
        chat_room.owner = self.request.user

        if commit:
            chat_room.save()

            chat_room.add_administrator(self.request.user)
            chat_room.add_users(self.cleaned_data["allowed_users"])

        return chat_room

    def clean_room_name(self):
        room_name = self.cleaned_data["room_name"].lower().strip().replace(" ", "_")
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        room_name = "".join([char for char in room_name if char in allowed])
        try:
            PrivateChatRoom.objects.get(room_name=room_name)
        except PrivateChatRoom.DoesNotExist:
            return room_name
        
        raise forms.ValidationError("A room with this name already exists :(")


class PrivateChatUpdateForm(forms.ModelForm):
    
    class Meta:
        model = PrivateChatRoom
        fields = ("room_name", "allowed_users", "administrators")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(PrivateChatUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        chat_room = super(PrivateChatUpdateForm, self).save(commit=False)
        chat_room.room_name = self.cleaned_data["room_name"]
        print(self.cleaned_data["administrators"])
        chat_room.administrators.set(self.cleaned_data["administrators"])
        chat_room.allowed_users.set(self.cleaned_data["allowed_users"])

        if commit:
            chat_room.save()

            chat_room.add_users(chat_room.administrators.all())
            chat_room.add_user(self.request.user)
            chat_room.add_administrator(self.request.user)
            chat_room.add_user(chat_room.owner)
            chat_room.add_administrator(chat_room.owner)

            chat_room.save()

        return chat_room
 
    def clean_room_name(self):
        room_name = self.cleaned_data["room_name"].lower().strip().replace(" ", "_")
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        room_name = "".join([char for char in room_name if char in allowed])
        try:
            PrivateChatRoom.objects.exclude(pk=self.instance.pk).get(room_name=room_name)
        except PrivateChatRoom.DoesNotExist:
            return room_name
        
        raise forms.ValidationError("A room with this name already exists :(")
