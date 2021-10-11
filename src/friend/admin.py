from django.contrib import admin

from .models import FriendList, FriendRequest


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id", "user")
    readonly_fields = ("id", "user")
    search_fields = ("id", "user")


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "is_active", "date_created")
    list_display_links = ("id", "sender", "receiver")
    readonly_fields = ("id", "sender", "receiver", "is_active", "date_created")
    list_filter = ("sender", "receiver", "is_active")
    search_fields = ("id", "sender", "receiver")