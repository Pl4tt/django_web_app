from typing import Any

from django.http import HttpResponse
from django.shortcuts import render

from .models import PublicMessage


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
        usable_pk_list = list(map(lambda x: x.pk, PublicMessage.objects.filter(pk__in=pk_value_list[:len(pk_value_list)-150])))
        print(PublicMessage.objects.filter(pk__in=usable_pk_list).all())
        PublicMessage.objects.filter(pk__in=usable_pk_list).all().delete()

    return render(request, "chat/public_chat.html", context)