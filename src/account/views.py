from typing import Union, Any

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect

from posts.views import check_likes
from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from .models import Account



def registration_view(request: Any, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    All about the registration form and it's validation.
    """
    context = {}

    if request.user.is_authenticated:
        return render(request, "error.html", {
            "error_message": f"You are already logged in as {request.user.username}."
        })

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect("posts:home")
        else:
            context["invalid_form"] = form
    return render(request, "account/registration.html", context)

def login_view(request: Any, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    All about the login form and it's validation.
    """
    context = {}

    if request.user.is_authenticated:
        return render(request, "error.html", {
            "error_message": f"You are already logged in as {request.user.username}."
        })

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"].lower()
            password = request.POST["password"]
            account = authenticate(email=email, password=password)
            if account:
                login(request, account)
                return redirect("posts:home")
        else:
            context["invalid_form"] = form

    return render(request, "account/login.html", context)

def logout_view(request: Any) -> HttpResponseRedirect:
    """
    loggs you out and redirects you to home.
    """
    logout(request)
    return redirect("posts:home")

def profile_view(request: Any, user_id: int) -> HttpResponse:
    """
    Renders profile of user if user exists.
    """
    context = {}
    user = request.user

    context["is_self"] = False
    if user.pk == user_id:
        context["is_self"] = True

    try:
        context["user"] = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
        
    return render(request, "account/profile_view.html", context)
    
def user_posts(request: Any, user_id: int) -> HttpResponse:
    """
    Returns a view with all posts of a user if the user exists.
    """
    context = {}
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
    context["user"] = user
    context["posts"] = [] # ((Post): post, (bool): user has liked post)
    
    for post in reversed(user.posts.all()):
        context["posts"].append((post, check_likes(request.user, post)))

    return render(request, "posts/post_view.html", context)

def user_likes(request: Any, user_id: int) -> HttpResponse:
    """
    Returns a view with all posts the user has liked if the user exists.
    """
    context = {}
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
    context["user"] = user
    context["posts"] = [] # ((Post): post, (bool): user has liked post)
    
    for like in reversed(user.likes.all()):
        context["posts"].append((like.post, check_likes(request.user, like.post)))

    return render(request, "posts/post_view.html", context)

def settings(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Renders the settings page from requested id if it's yourself and saves the changes if there are changes.
    """
    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    req_user = request.user
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })

    if user.pk != req_user.pk:
        return render(request, "error.html", {
            "error_message": "You are not allowed to change someone else's account."
        })
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=req_user)
        if form.is_valid():
            form.save()
            return redirect("account:profile", user_id=req_user.pk)
        else:
            context["error"] = "Form is invalid!"

    context["user"] = req_user

    return render(request, "account/settings.html", context)

def search(request: Any, *args, **kwargs) -> HttpResponse:
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