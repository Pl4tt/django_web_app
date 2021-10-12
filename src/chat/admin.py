from django.contrib import admin

from .models import PublicMessage, PrivateMessage, PrivateChatRoom



@admin.register(PrivateChatRoom)
class PrivateChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_name", "owner", "date_created")
    list_display_links = ("id", "room_name", "owner")
    readonly_fields = ("id", "owner", "date_created")
    list_filter = ("owner",)
    search_fields = ("id", "room_name", "owner", )


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "chat_room", "date_created")
    list_display_links = ("id", "author", "chat_room")
    readonly_fields = ("id", "author", "chat_room", "content", "date_created")
    list_filter = ("author", "chat_room")
    search_fields = ("id", "content")


@admin.register(PublicMessage)
class PublicMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created")
    list_display_links = ("id", "author", "date_created")
    readonly_fields = ("id", "author", "content", "date_created")
    search_fields = ("id", "content")
    list_filter = ("author",)