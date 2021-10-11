from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created")
    list_display_links = ("id", "author", "date_created")
    readonly_fields = ("id", "author", "content", "date_created")
    search_fields = ("id", "content")
    filter_fields = ("author",)