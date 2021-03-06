from django.urls import path


from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("like-post/<int:post_id>/", views.like_post, name="like_post"),
    path("comment-post/<int:post_id>/<str:comment_content>/", views.comment_post, name="comment_post"),
    path("edit-post/<int:post_id>/<str:new_post_content>/", views.edit_post, name="edit_post"),
    path("delete-comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
]