from typing import Any, Union

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from account.views import get_past_position
from .models import FriendList, FriendRequest


USER_MODEL = get_user_model()


def check_friend(user1: settings.AUTH_USER_MODEL, user2: settings.AUTH_USER_MODEL) -> bool:
    """
    Returns True if user1 is a friend of user2 else False.
    """
    return user1 in user2.friend_list.friends.all()


def helper_friend(request, user_id: int, friend_request=None):
    """
    Validates the user_id and friend_request and returns both.
    """

    try:
        user = USER_MODEL.objects.get(pk=user_id)
    except USER_MODEL.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "User doesn't exist."
        })
    
    if friend_request:
        try:
            friend_request = FriendRequest.objects.get(sender=user, receiver=request.user)
        except FriendRequest.DoesNotExist:
            return render(request, "error.html", {
                "error_message": "Friend Request not found :("
            })
    
    return (user, friend_request)



@login_required
def friend_list(request: Any, user_id: int) -> HttpResponse:
    """
    Returns a view with all friends of the user with the given user_id.
    Only accessable for friends of the given user.
    """
    context = {}

    user, _ = helper_friend(request, user_id)

    if request.user.pk != user.pk and not check_friend(request.user, user):
        return render(request, "error.html", {
            "error_message": "You are not allowed to see friends of a non-friends."
        })
    
    context["friend_list"] = FriendList.objects.get(user=user).friends.all()
    context["user"] = user

    return render(request, "friend/friend_list.html", context)

@login_required
def accept_request(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Accepts the friend request sent from the user with the given user_id to the request user.
    """
    context = {}

    try:
        user, friend_request = helper_friend(request, user_id, friend_request=True)
    except ValueError:
        return helper_friend(request, user_id, friend_request=True)
    
    friend_request.accept()

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)
    
@login_required
def decline_request(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Declines the friend request sent from the user with the given user_id to the request user.
    """
    context = {}

    try:
        user, friend_request = helper_friend(request, user_id, friend_request=True)
    except ValueError:
        return helper_friend(request, user_id, friend_request=True)
    
    friend_request.decline()

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)

@login_required
def cancel_request(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Cancels the friend request sent from the request user to the user with the given user_id.
    """
    context = {}

    try:
        user, _ = helper_friend(request, user_id)
    except ValueError:
        return helper_friend(request, user_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=request.user, receiver=user)
    except FriendRequest.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Friend Request not found :("
        })

    friend_request.cancel()

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)

@login_required
def create_request(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Trys to reactivate a friend request sent from the request user to the user with the given user_id.
    If there is no Friend Request, it creates a new one.
    """
    context = {}

    try:
        user, _ = helper_friend(request, user_id)
    except ValueError:
        return helper_friend(request, user_id)

    try:
        friend_request = FriendRequest.objects.get(sender=request.user, receiver=user)
        friend_request.reactivate()
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=request.user, receiver=user)
        friend_request.save()

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)

@login_required
def unfriend(request: Any, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Removes the user with the given user_id to the friend list of the request user
    and removes the request user to the friend list of the given user_id.
    """
    context = {}

    try:
        user, _ = helper_friend(request, user_id)
    except ValueError:
        return helper_friend(request, user_id)
    
    friend_list = request.user.friend_list
    friend_list.unfriend(user)

    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("account:profile", user_id=user_id)