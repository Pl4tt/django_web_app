from typing import Any, Union

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import PublicMessage, PrivateMessage, PrivateChatRoom
from .forms import ChatRoomCreationForm, PrivateChatUpdateForm


def public_chat(request: Any, *args, **kwargs) -> HttpResponse:
    """
    Returns the public chat view (containing a websocket) and sends the latest 75 messages in db to the template.
    If there are more then 150 messages in the database, they will get deleted.
    """
    context = {}
    messages = sorted(list(PublicMessage.objects.all()), key=lambda msg: msg.pk)
    context["messages"] = list(messages)[-75:]

    if len(messages) > 150:
        pk_value_list = sorted(list(PublicMessage.objects.values_list("pk", flat=True)))
        usable_pk_list = list(map(lambda x: x.pk, PublicMessage.objects.filter(pk__in=pk_value_list[:-150])))
        PublicMessage.objects.filter(pk__in=usable_pk_list).all().delete()

    return render(request, "chat/public_chat.html", context)

@login_required
def private_chat(request: Any, chat_id: int, *args, **kwargs) -> HttpResponse:
    """
    Validates the user and the chat and returns the chat view.
    """
    context = {}

    try:
        chat = PrivateChatRoom.objects.get(pk=chat_id)
    except PrivateChatRoom.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Chat Room doesn't exist."
        })
    
    if not chat.check_user(request.user):
        return render(request, "error.html", {
            "error_message": "You are not authenticated to see this Chat."
        })

    messages = sorted(PrivateMessage.objects.filter(chat_room=chat).all(), key=lambda msg: msg.pk)
    context["messages"] = messages[-100:]
    context["room_name"] = chat.room_name
    context["chat_id"] = chat_id
    context["chat_room"] = chat

    if len(messages) > 200:
        PrivateMessage.objects.filter(pk__in=list(map(lambda msg: msg.pk, messages)[:-200])).all().delete()

    return render(request, "chat/private_chat.html", context)

@login_required
def create_private_chat(request: Any) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Validates the creation form and creates a private chat if no errors.
    """
    context = {}

    if request.POST:
        form = ChatRoomCreationForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("chat:chat_overview")
        else:
            context["invalid_form"] = form

    context["users"] = get_user_model().objects.exclude(pk=request.user.pk).all()
    context["what"] = "private"

    return render(request, "chat/chat_creation.html", context)

@login_required
def chat_overview(request: Any) -> HttpResponse:
    """
    Returns a list view with all private chats of the request user.
    """
    context = {}
    context["user"] = request.user
    context["chat_list"] = request.user.private_chats.all()

    return render(request, "chat/chat_overview.html", context)

@login_required
def edit_private_chat(request: Any, chat_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    
    """
    context = {}

    try:
        chat_room = PrivateChatRoom.objects.get(pk=chat_id)
    except PrivateChatRoom.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Chat with the given id doesn't exist."
        })

    if request.user != chat_room.owner and not chat_room.check_admin(request.user):
        return render(request, "error.html", {
            "error_message": "You are not authenticated to edit this chat."
        })

    if request.POST:
        form = PrivateChatUpdateForm(request.POST, request=request, instance=chat_room)
        if form.is_valid():
            form.save()
            return redirect("chat:private_chat", chat_id=chat_id)
        else:
            context["invalid_form"] = form

    context["users"] = get_user_model().objects.exclude(pk=request.user.pk).all()
    context["what"] = "private"
    context["chat"] = chat_room

    return render(request, "chat/edit_chat.html", context)

@login_required
def delete_private_chat(request: Any, chat_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Deletes the given chat if the user is authenticated to do that.
    """
    context = {}

    try:
        chat_room = PrivateChatRoom.objects.get(pk=chat_id)
    except PrivateChatRoom.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Chatroom doesn't exist."
        })

    if request.user != chat_room.owner:
        return render(request, "error.html", {
            "error_message": "Only the owner of the chatroom is authenticated to do that."
        })
    
    chat_room.delete()

    return redirect("chat:chat_overview")

@login_required
def leave_private_chat(request: Any, chat_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Removes the request user from the given chat.
    """
    context = {}

    try:
        chat_room = PrivateChatRoom.objects.get(pk=chat_id)
    except PrivateChatRoom.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Chatroom doesn't exist."
        })
    
    chat_room.remove_user(request.user)

    return redirect("chat:chat_overview")