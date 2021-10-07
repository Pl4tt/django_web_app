from django.urls import path

from . import views


app_name = "chat"

urlpatterns = [
    path("public/", views.public_chat, name="public_chat"),
]