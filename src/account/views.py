from django.shortcuts import render, redirect
from django.contrib.auth import logout


def registration_view(request):
    context = {}
    if request.POST:
        pass
    return render(request, "account/registration.html", context)

def login_view(request):
    context = {}
    if request.POST:
        pass
    return render(request, "account/login.html", context)

def _logout(request):
    logout(request)
    return redirect("public_chat")