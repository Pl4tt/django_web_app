from django.urls import path

from . import views


app_name = "chat"

urlpatterns = [
    path("public/", views.public_chat, name="public_chat"),
    path("private/<int:chat_id>/", views.private_chat, name="private_chat"),
    path("chat-overview/", views.chat_overview, name="chat_overview"),
    path("create/private/", views.create_private_chat, name="create_private_chat"),
    path("edit/private/<int:chat_id>/", views.edit_private_chat, name="edit_private_chat"),
    path("leave/private/<int:chat_id>/", views.leave_private_chat, name="leave_private_chat"),
    path("delete/private/<int:chat_id>/", views.delete_private_chat, name="delete_private_chat"),
]