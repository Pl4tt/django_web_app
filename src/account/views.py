from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse

from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from .models import Account



def get_redirect_if_exists(request):
    """
    gets your past position if exists.
    """
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    
    return redirect


def registration_view(request, *args, **kwargs):
    """
    All about the registration form and it's validation.
    """
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
    """
    All about the login form and it's validation.
    """
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
    """
    loggs you out and redirects you to home.
    """
    logout(request)
    return redirect("posts:home")

def profile_view(request, id: int):
    """
    Renders profile of user if user exists.
    """
    context = {}
    user = request.user

    context["is_self"] = False
    if user.pk == id:
        context["is_self"] = True

    try:
        context["user"] = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return HttpResponse("User doesn't exists")
    return render(request, "account/profile_view.html", context)

def settings(request, id: int):
    """
    Renders the settings page from requested id if it's yourself and saves the changes if there are changes.
    """
    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    req_user = request.user
    try:
        user = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return HttpResponse("User doesn't exist")

    if user.pk != req_user.pk:
        return HttpResponse("You are not allowed to change someone else's account")
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=req_user)
        if form.is_valid():
            form.save()
            return redirect("account:profile", id=req_user.pk)
        else:
            context["error"] = "Form is invalid!"

    context["user"] = req_user

    return render(request, "account/settings.html", context)

def search(request, *args, **kwargs):
    """
    Renders the search results.
    """
    context = {}

    if request.GET:
        query = request.GET["q"]
        accounts = Account.objects.filter(username__icontains=query).distinct()
        search_results = []

        for account in accounts:
            search_results.append((account, False)) # TODO: replace false with is_friend when created friend system

        context["search_results"] = search_results
        context["query"] = query
    
    return render(request, "account/search_results.html", context)