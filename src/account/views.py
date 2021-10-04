from django.shortcuts import render, redirect
from django.contrib.auth import logout


def _logout(request):
    logout(request)
    return redirect("public_chat")