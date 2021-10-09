from django.urls import path


from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),
]