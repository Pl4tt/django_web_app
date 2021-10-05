from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views._logout, name="logout"),
]