from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.registration_view, name="register"),
    path("account/<int:id>/", views.profile_view, name="profile"),
    path("settings/<int:id>/", views.settings, name="settings"),
]