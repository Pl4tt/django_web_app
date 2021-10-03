from django.shortcuts import render


def public_chat(request, *args, **kwargs):
    context = {}
    return render(request, "public_chat/public_chat.html", context)