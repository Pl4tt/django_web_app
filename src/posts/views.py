from typing import Union, Any

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Post, Comment, Like


def home_view(request: Any) -> HttpResponse:
    """
    Returns the view where all posts, comments etc. are viewed.
    """
    context = {}
    context["posts"] = reversed(Post.objects.all())
    return render(request, "posts/post_view.html", context)

def create_post(request: Any) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Returns the view where useres can create posts if they are authenticated.
    After they've created their post, the will be redirected to the home view.
    """
    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("account:login")

    if request.POST:
        post_content = request.POST["post_content"]

        if not post_content:
            return render(request, "posts/create_post.html", context)

        post = Post(content=post_content, author=user)
        post.save()
        return redirect("posts:home")
    
    return render(request, "posts/create_post.html", context)