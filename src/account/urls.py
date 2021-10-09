from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/<int:id>/", views.profile_view, name="profile"),
    path("user_posts/<int:id>/", views.user_posts, name="user_posts"),
    path("settings/<int:id>/", views.settings, name="settings"),
    path("search/", views.search, name="search"),
]