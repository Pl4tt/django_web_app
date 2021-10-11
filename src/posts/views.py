from typing import Union, Any

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Like


def get_past_position(request: Any):
    """
    gets the users past position if exists.
    """
    return request.META.get('HTTP_REFERER')


def check_likes(user: settings.AUTH_USER_MODEL, post: Post) -> bool:
    """
    Returns True if the user has liked the post else false
    """
    return user in map(lambda like: like.author, post.likes.all())


def home_view(request: Any) -> HttpResponse:
    """
    Returns the view where all posts, comments etc. are viewed.
    """
    context = {}
    context["posts"] = [] # ((Post): post, (bool): user has liked post)
    
    for post in reversed(Post.objects.all()):
        context["posts"].append((post, check_likes(request.user, post)))

    return render(request, "posts/post_view.html", context)

@login_required
def create_post(request: Any) -> HttpResponse:
    """
    Returns the view where useres can create posts if they are authenticated.
    After they've created their post, the will be redirected to the home view.
    """
    context = {}
    user = request.user

    if request.POST:
        post_content = request.POST.get("post_content")
        post_content = post_content.strip()

        if not post_content:
            return render(request, "posts/create_post.html", context)

        post = Post(content=post_content, author=user)
        post.save()
        return redirect("posts:home")
    
    return render(request, "posts/create_post.html", context)

@login_required
def delete_post(request: Any, post_id: int) -> Union[HttpResponseRedirect, HttpResponse]:
    """
    Deletes the post with the given id if it exists and user is authenticated and redirects User to his past url.
    """
    user = request.user


    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "The post with the given id does not exist."
        })
    
    if user.pk != post.author.pk:
        return render(request, "error.html", {
            "error_message": "You are not allowed to delete someone else's post"
        })

    post.delete()
    
    destination = get_past_position(request)
    if destination:
        return redirect(destination)
    return redirect("posts:home")

@login_required
def like_post(request: Any, post_id: int) -> Union[JsonResponse, HttpResponse]:
    """
    Returns a json response containing a boolean if the user has liked the post and the number of likes.
    """
    user = request.user
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Post doesn't exist."
        })
        
    like = Like.objects.filter(author=user, post=post)
    
    if like:
        like.delete()
    else:
        like = Like(post=post, author=user)
        like.save()
        
    json_data = {
        "like_count": len(post.likes.all()),
        "liked": check_likes(user, post),
    }
    
    return JsonResponse(json_data)

@login_required
def comment_post(request: Any, post_id: int, comment_content: str) -> Union[JsonResponse, HttpResponse, HttpResponseRedirect]:
    """
    Returns a json response containing the new length of all comments in this post the comment itself if the user and post exist.
    """
    user = request.user

    comment_content = comment_content.strip()

    if not comment_content:
        destination = get_past_position(request)
        if destination:
            return redirect(destination)
        return redirect("posts:home")
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "Post doesn't exist."
        })
    
    comment = Comment(content=comment_content, author=user, post=post)
    comment.save()

    json_data = {
        "comment_count": len(post.comments.all()),
        "comment_content": comment.content,
        "comment_author_username": comment.author.username,
        "comment_author_pk": comment.author.pk,
        "comment_author_profile_image_url": comment.author.profile_image.url,
        "comment_date_created": comment.date_created,
    }

    return JsonResponse(json_data)

@login_required
def edit_post(request: Any, post_id: int, new_post_content: str) -> Union[JsonResponse, HttpResponse, HttpResponseRedirect]:
    """
    Changes the content of the post with pk=post_id and returns a json response containing the new post content
    if the user is allowed to do that.
    """
    user = request.user

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, "error.html", {
            "error_message": "The Post you tried to edit doesn't exist."
        })
    
    if user.pk != post.author.pk:
        return render(request, "error.html", {
            "error_message": "You are not allowed to edit someone else's post."
        })
    
    new_post_content = new_post_content.strip()

    post.content = new_post_content
    post.save()

    json_data = {
        "new_content": new_post_content,
    }

    return JsonResponse(json_data)