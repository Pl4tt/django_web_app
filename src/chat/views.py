from django.shortcuts import render


def public_chat(request, *args, **kwargs):
    context = {"messages": ["hi"]}
    # TODO: context["messages"] = all message elements from database
    return render(request, "chat/public_chat.html", context)