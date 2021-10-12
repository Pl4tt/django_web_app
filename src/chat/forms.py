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

        if commit:
            chat_room.save()

        chat_room.owner = self.request.user
        chat_room.add_administrator(self.request.user)
        chat_room.add_users(self.cleaned_data["allowed_users"])
        
        if commit:
            chat_room.save()
        return chat_room

    def clean_room_name(self):
        room_name = self.cleaned_data["room_name"].lower()
        try:
            PrivateChatRoom.objects.get(room_name=room_name)
        except PrivateChatRoom.DoesNotExist:
            return room_name
        
        raise forms.ValidationError("A room with this name already exists :(")
