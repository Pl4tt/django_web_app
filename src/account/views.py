from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse

from .forms import AccountAuthenticationForm, RegistrationForm
from .models import Account



def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    
    return redirect


def registration_view(request, *args, **kwargs):
    context = {}

    if request.user.is_authenticated:
        return HttpResponse(f"You are already logged in as {request.user.username}.")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            account = authenticate(email=email, password=password)
            login(request, account)

            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("chat:public_chat")
        else:
            context["invalid_form"] = form
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
            context["invalid_form"] = form

    return render(request, "account/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("chat:public_chat")

def profile_view(request, id: int):
    context = {}
    context["user"] = Account.objects.get(pk=id)
    return render(request, "account/profile_view.html", context)