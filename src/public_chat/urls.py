from django.urls import path

from . import views

urlpatterns = [
    path("", views.public_chat, name="public_chat"),
]