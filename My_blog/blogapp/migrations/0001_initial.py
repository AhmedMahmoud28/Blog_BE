# Generated by Django 4.1.1 on 2023-09-26 17:27

import My_blog.services.helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=200, verbose_name="Slug")),
                (
                    "image",
                    models.ImageField(
                        upload_to=functools.partial(
                            My_blog.services.helpers.file_upload, *("blog",), **{}
                        )
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=200, verbose_name="Slug")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=functools.partial(
                            My_blog.services.helpers.file_upload,
                            *("blog_category",),
                            **{}
                        ),
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog category",
                "verbose_name_plural": "Blog categories",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("text", models.TextField()),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=functools.partial(
                            My_blog.services.helpers.file_upload,
                            *("post_pictures",),
                            **{}
                        ),
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogapp.blog"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogapp.post"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=functools.partial(
                            My_blog.services.helpers.file_upload,
                            *("comment_pictures",),
                            **{}
                        ),
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogapp.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlogSection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", tinymce.models.HTMLField()),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=functools.partial(
                            My_blog.services.helpers.file_upload,
                            *("blog_section",),
                            **{}
                        ),
                    ),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blogapp.blog",
                        verbose_name="Blog",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="blog",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="blogapp.blogcategory",
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="related_blogs",
            field=models.ManyToManyField(blank=True, to="blogapp.blog"),
        ),
        migrations.CreateModel(
            name="PostLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogapp.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post Like",
                "verbose_name_plural": "Posts Likes",
                "unique_together": {("user", "post")},
            },
        ),
        migrations.CreateModel(
            name="CommentLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blogapp.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment Like",
                "verbose_name_plural": "Comments Likes",
                "unique_together": {("user", "comment")},
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogapp.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "post")},
            },
        ),
    ]
