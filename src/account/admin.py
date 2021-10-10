from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Account, Follow


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ("id", "username", "email", "date_created", "last_login", "is_admin", "is_staff")
    list_display_links = ("id", "username", "email")
    list_filter = ("is_admin", "is_staff", "is_superuser", "is_active", "hide_email")
    readonly_fields = ("id", "date_created", "last_login")
    search_fields = ("id", "username", "email")

    filter_horizontal = ()
    fieldsets = ()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "following_user", "followed_user", "date_created")
    list_display_links = ("id", "following_user", "followed_user")
    list_filter = ("following_user", "followed_user")
    readonly_fields = ("id", "following_user", "followed_user", "date_created")
    search_fields = ("id",)

