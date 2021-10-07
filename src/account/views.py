from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse

from .forms import AccountAuthenticationForm



def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    
    return redirect


def registration_view(request, *args, **kwargs):
    context = {}
    if request.POST:
        pass
    return render(request, "account/registration.html", context)

def login_view(request, *args, **kwargs):
    context = {}

    if request.user.is_authenticated:
        return HttpResponse(f"You are already logged in as {request.user.username}.")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"].lower()
            password = request.POST["password"]
            account = authenticate(email=email, password=password)
            if account:
                login(request, account)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("chat:public_chat")
        else:
            context["wrong_form"] = form

    return render(request, "account/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("chat:public_chat")