from django.shortcuts import render


def public_chat(request, *args, **kwargs):
    context = {}
    return render(request, "chat/public_chat.html", context)