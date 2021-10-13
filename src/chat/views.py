from typing import Any

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import PublicMessage, PrivateMessage, PrivateChatRoom
from .forms import ChatRoomCreationForm


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

    if len(messages) > 200:
        PrivateMessage.objects.filter(pk__in=list(map(lambda msg: msg.pk, messages)[:-200])).all().delete()

    return render(request, "chat/private_chat.html", context)

@login_required
def create_private_chat(request: Any) -> HttpResponse:
    """
    Validates the creation form and creates a private chat if no errors.
    """
    context = {}

    if request.POST:
        form = ChatRoomCreationForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("posts:home") # TODO: redirect to list of all his chats
        else:
            context["invalid_form"] = form

    context["users"] = get_user_model().objects.exclude(pk=request.user.pk).all()
    context["what"] = "private"

    return render(request, "chat/chat_creation.html", context)