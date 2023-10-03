from django.contrib import admin

from . import models

# from django.utils.translation import gettext_lazy as _


""" Blog """


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["user", "following"]


@admin.register(models.BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["id", "name", "image"]


@admin.register(models.Blog)
class Blog(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["id", "title", "image"]


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title"]


@admin.register(models.PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "post",
    ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post"]


@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "comment"]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post"]
