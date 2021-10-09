from django.contrib import admin

from .models import Post, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "date_created")
    list_display_links = ("id", "author")
    list_filter = ("author",)
    readonly_fields = ("id", "date_created")
    search_fields = ("id", "content")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "date_created")
    list_display_links = ("id", "author", "post")
    list_filter = ("author", "post")
    readonly_fields = ("id", "author", "post", "date_created")
    search_fields = ("id", "content")


class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "date_created")
    list_display_links = ("id", "author", "post")
    list_filter = ("author", "post")
    readonly_fields = ("id", "author", "post", "date_created")
    search_fields = ("id",)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

