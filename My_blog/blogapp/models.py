from functools import partial

from django.db import models

# from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from My_blog.services.helpers import file_upload
from My_blog.userapp.models import User

# from tinymce.models import HTMLField


class TestNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following_users"
    )

    class Meta:
        unique_together = ("user", "following")

    def __str__(self):
        return f"{self.user, self.following}"


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(_("Slug"), max_length=200)
    image = models.ImageField(
        upload_to=partial(file_upload, "blog_category"), null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog category"
        verbose_name_plural = "Blog categories"


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(_("Slug"), max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=partial(file_upload, "blog"))
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    related_blogs = models.ManyToManyField("self", blank=True)
    category = models.ForeignKey("BlogCategory", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("name",)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    picture = models.ImageField(
        upload_to=partial(file_upload, "post_pictures"), null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "post",
        )
        verbose_name = "Post Like"
        verbose_name_plural = "Posts Likes"

    def __str__(self):
        return f"{self.user, self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.TextField()
    picture = models.ImageField(
        upload_to=partial(file_upload, "comment_pictures"), null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "comment",
        )
        verbose_name = "Comment Like"
        verbose_name_plural = "Comments Likes"

    def __str__(self):
        return f"{self.user, self.comment}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "post",
        )

    def __str__(self):
        return f"{self.user, self.post}"
