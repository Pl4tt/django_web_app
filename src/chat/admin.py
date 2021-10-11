from django.contrib import admin

from .models import PublicMessage


@admin.register(PublicMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created")
    list_display_links = ("id", "author", "date_created")
    readonly_fields = ("id", "author", "content", "date_created")
    search_fields = ("id", "content")
    list_filter = ("author",)