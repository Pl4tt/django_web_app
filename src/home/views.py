from django.shortcuts import render


def home(request, *args, **kwargs):
    context = {}
    return render(request, "home/home.html", context)