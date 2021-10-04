from django.urls import path

from . import views


urlpatterns = [
    path("logout/", views._logout, name="logout")
]