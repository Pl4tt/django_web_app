from django.urls import path

from . import views


app_name = "friend"

urlpatterns = [
    path("friend-list/<int:user_id>/", views.friend_list, name="friend_list"),
    path("unfriend/<int:user_id>/", views.unfriend, name="unfriend"),
    path("accept/<int:user_id>/", views.accept_request, name="accept_request"),
    path("decline/<int:user_id>/", views.decline_request, name="decline_request"),
    path("cancel/<int:user_id>/", views.cancel_request, name="cancel_request"),
    path("create_request/<int:user_id>/", views.create_request, name="create_request"),
]