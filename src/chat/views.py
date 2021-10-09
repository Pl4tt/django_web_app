from typing import Any

from django.http import HttpResponse
from django.shortcuts import render


def public_chat(request: Any, *args, **kwargs) -> HttpResponse:
    context = {"messages": ["hi"]}
    # TODO: context["messages"] = all message elements from database
    return render(request, "chat/public_chat.html", context)