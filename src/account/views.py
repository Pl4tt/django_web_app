from typing import Union, Any

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from posts.views import check_likes, get_past_position
from friend.views import check_friend
from friend.models import FriendRequest
from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from .models import Account, Follow


def check_follow(user1: Account, user2: Account) -> bool:
    """
    Returns True if user1 follows user2 else False.
    """
    return user2 in user1.followers.all()


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
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
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
            email = request.POST.get("email").lower()
            password = request.POST.get("password")
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
    print(request.user.friend_list.friends.all())

    try:
        context["user"] = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
    
    if request.user.is_authenticated:
        context["is_self"] = request.user.pk == user_id
        context["is_friend"] = check_friend(request.user, context["user"])
        context["is_friend_requested"] = False
        context["is_friend_requesting"] = False

        if FriendRequest.objects.filter(sender=context["user"], receiver=request.user, is_active=True):
            context["is_friend_requesting"] = True

        if FriendRequest.objects.filter(sender=request.user, receiver=context["user"], is_active=True):
            context["is_friend_requested"] = True

    context["follower"] = list(map(lambda follow: follow.following_user, context["user"].follower.all()))
        
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
    
    for post in user.posts.all():
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
    
    for like in reversed(sorted(user.likes.all(), key=lambda like: like.post.date_created)):
        context["posts"].append((like.post, check_likes(request.user, like.post)))

    return render(request, "posts/post_view.html", context)

def user_comments(request: Any, user_id: int) -> HttpResponse:
    """
    Returns a view with all posts the user has commented if the user exists.
    """
    context = {}
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User does not exist."
        })
    context["user"] = user
    context["posts"] = [] # ((Post): post, (bool): user has liked post)

    for comment in reversed(sorted(user.comments.all(), key=lambda comment: comment.post.date_created)):
        if not (temp := (comment.post, check_likes(request.user, comment.post))) in context["posts"]:
            context["posts"].append(temp)
    
    return render(request, "posts/post_view.html", context)

@login_required
def settings(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Renders the settings page from requested id if it's yourself and saves the changes if there are changes.
    """

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
        query = request.GET.get("q")
        accounts = Account.objects.filter(username__icontains=query).distinct()
        search_results = []

        for account in accounts:
            search_results.append((account, False)) # TODO: replace false with is_friend when created friend system

        context["search_results"] = search_results
        context["query"] = query
    
    return render(request, "account/search_results.html", context)

@login_required
def follow(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Add the request user to the followers of the user with the given user_id.
    Returns the given users profile view after that.
    """
    context = {}

    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
    
    if request.user.pk == user.pk:
        return render(request, "error.html", {
            "error_message": "You are not allowed to follow yourself."
        })
    
    follow = Follow.objects.filter(following_user=request.user, followed_user=user)

    if follow:
        follow.delete()
    else:
        follow = Follow(following_user=request.user, followed_user=user)
        follow.save()

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)

def follow_view(request: Any, user_id: int, what: str) -> HttpResponse:
    """
    If what == "follower": Returns a view of all the users that follow the user (with pk=user_id).
    If what == "following": Returns a view of all the users that the user (with pkk=user_id) is following.
    """
    context = {}
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })

    if what == "follower":
        context["list"] = zip(getattr(user, what).all(), list(map(lambda follow: getattr(follow, "following_user"), getattr(user, what).all())))
    elif what == "following":
        context["list"] = zip(getattr(user, what).all(), list(map(lambda follow: getattr(follow, "followed_user"), getattr(user, what).all())))
    else:
        return render(request, "404.html")

    context["what"] = what
    context["user"] = user
    
    return render(request, "account/follow_view.html", context)