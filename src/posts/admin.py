from django.contrib import admin

from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created")
    list_display_links = ("id", "author")
    list_filter = ("author",)
    readonly_fields = ("content", "id", "author", "date_created")
    search_fields = ("id", "content")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "date_created")
    list_display_links = ("id", "author", "post")
    list_filter = ("author", "post")
    readonly_fields = ("content", "id", "author", "post", "date_created")
    search_fields = ("id", "content")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "date_created")
    list_display_links = ("id", "author", "post")
    list_filter = ("author", "post")
    readonly_fields = ("id", "author", "post", "date_created")
    search_fields = ("id",)



