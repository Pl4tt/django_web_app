from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/<int:user_id>/", views.profile_view, name="profile"),
    path("user-posts/<int:user_id>/", views.user_posts, name="user_posts"),
    path("user-likes/<int:user_id>/", views.user_likes, name="user_likes"),
    path("user-comments/<int:user_id>/", views.user_comments, name="user_comments"),
    path("settings/<int:user_id>/", views.settings, name="settings"),
    path("search/", views.search, name="search"),
]