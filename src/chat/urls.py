from django.urls import path

from . import views


app_name = "chat"

urlpatterns = [
    path("public/", views.public_chat, name="public_chat"),
    path("private/<int:chat_id>/", views.private_chat, name="private_chat"),
    path("create/private/", views.create_private_chat, name="create_private_chat"),
]