from django.db import transaction
from django.db.models import Count
from rest_framework import serializers

from My_blog.blogapp import models
from My_blog.userapp.serializers import UserDataSerializer


class FollowerSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()

    class Meta:
        model = models.Follow
        fields = [
            "id",
            "user",
        ]


class FollowSerializer(serializers.ModelSerializer):
    following = UserDataSerializer()

    class Meta:
        model = models.Follow
        fields = [
            "id",
            "following",
        ]


class AddFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = [
            "following",
        ]

    def save(self, **kwargs):
        with transaction.atomic():
            user = self.context["user"]
            following = self.validated_data["following"]
            if user == following:
                raise serializers.ValidationError()
            self.instance = models.Follow.objects.create(
                user=user,
                following=following,
            )
        return self.instance


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogCategory
        fields = "__all__"


# simple serializer
class BlogCategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogCategory
        fields = (
            "id",
            "name",
        )


# simple serializer
class BlogDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = (
            "id",
            "title",
        )


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = (
            "id",
            "title",
            "slug",
            "created_by",
            "image",
            "description",
        )


class BlogDetailedSerializer(serializers.ModelSerializer):
    related_blogs = BlogDataSerializer(many=True)
    category = BlogCategoryDataSerializer()
    date = serializers.SerializerMethodField()
    created_by = UserDataSerializer()

    class Meta:
        model = models.Blog
        exclude = ("slug",)

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField(method_name="booked")
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Post
        fields = "__all__"

    def booked(self, obj):
        return obj.id in models.Bookmark.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def like(self, obj):
        return obj.id in models.PostLike.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def likecount(self, obj):
        Q = (
            models.PostLike.objects.select_related("post")
            .values("post")
            .annotate(Count("post"))
        )
        for i in Q:
            if obj.id == i["post"]:
                return i["post__count"]
        else:
            return 0

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")


class PostSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField(method_name="booked")
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Post
        fields = [
            "id",
            "date",
            "title",
            "text",
            "picture",
            "blog",
            "tags",
            "is_bookmarked",
            "is_liked",
            "likes",
        ]

    def booked(self, obj):
        return obj.id in models.Bookmark.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def like(self, obj):
        return obj.id in models.PostLike.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def likecount(self, obj):
        Q = (
            models.PostLike.objects.select_related("post")
            .values("post")
            .annotate(Count("post"))
        )
        for i in Q:
            if obj.id == i["post"]:
                return i["post__count"]
        else:
            return 0

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")


class PostDetailedSerializer(serializers.ModelSerializer):
    blog = BlogDataSerializer()
    user = UserDataSerializer(read_only=True)
    date = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField(method_name="postcomments")
    is_bookmarked = serializers.SerializerMethodField(method_name="booked")
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Post
        fields = (
            "user",
            "title",
            "date",
            "blog",
            "tags",
            "text",
            "picture",
            "comments",
            "is_bookmarked",
            "is_liked",
            "likes",
        )

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")

    def booked(self, obj):
        return obj.id in models.Bookmark.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def like(self, obj):
        return obj.id in models.PostLike.objects.filter(
            user=self.context["user"]
        ).values_list("post", flat=True)

    def likecount(self, obj):
        Q = (
            models.PostLike.objects.select_related("post")
            .values("post")
            .annotate(Count("post"))
        )
        for i in Q:
            if obj.id == i["post"]:
                return i["post__count"]
        else:
            return 0

    def postcomments(self, obj):
        Query = models.Comment.objects.select_related("user").filter(post=obj)
        return CommentSerializer(Query, many=True).data


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = [
            "id",
            "blog",
            "title",
            "text",
            "tags",
            "picture",
            "date",
        ]

    def save(self, **kwargs):
        with transaction.atomic():
            self.instance = models.Post.objects.create(
                user=self.context["user"],
                title=self.validated_data["title"],
                blog=self.validated_data["blog"],
                text=self.validated_data["text"],
                picture=self.validated_data["picture"],
            )
            tags = self.validated_data.get("tags")
            if tags:
                self.instance.tags.set(tags)
        return self.instance


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = [
            "blog",
            "title",
            "text",
            "tags",
            "picture",
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = models.PostLike
        exclude = ("user",)


class AddPostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ("id", "post")

    def save(self, **kwargs):
        with transaction.atomic():
            self.instance = models.PostLike.objects.filter(
                user=self.context["user"], post=self.validated_data["post"]
            ).first()
            if self.instance is None:
                return models.PostLike.objects.create(
                    user_id=self.context["user"], post=self.validated_data["post"]
                )


class UpdatePostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ("id", "post")


class CommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "user",
            "post",
            "text",
            "picture",
            "date_created",
            "is_liked",
            "likes",
        )

    def like(self, obj):
        return obj.id in models.CommentLike.objects.filter(
            user=self.context["user"]
        ).values_list("comment", flat=True)

    def likecount(self, obj):
        Q = (
            models.CommentLike.objects.select_related("comment")
            .values("comment")
            .annotate(Count("comment"))
        )
        for i in Q:
            if obj.id == i["comment"]:
                return i["comment__count"]
        else:
            return 0


class CommentDetailedSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Comment
        exclude = ("user",)

    def like(self, obj):
        return obj.id in models.CommentLike.objects.filter(
            user=self.context["user"]
        ).values_list("comment", flat=True)

    def likecount(self, obj):
        Q = (
            models.CommentLike.objects.select_related("comment")
            .values("comment")
            .annotate(Count("comment"))
        )
        for i in Q:
            if obj.id == i["comment"]:
                return i["comment__count"]
        else:
            return 0


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("post", "text", "picture")

    def save(self, **kwargs):
        with transaction.atomic():
            return models.Comment.objects.create(
                user=self.context["user"],
                post=self.validated_data["post"],
                text=self.validated_data["text"],
                picture=self.validated_data["picture"],
            )


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("post", "text", "picture")


class CommentLikeSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()

    class Meta:
        model = models.CommentLike
        exclude = ("user",)


class AddCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = ("id", "comment")

    def save(self, **kwargs):
        with transaction.atomic():
            self.instance = models.CommentLike.objects.filter(
                user=self.context["user"], comment=self.validated_data["comment"]
            ).first()
            if self.instance is None:
                return models.CommentLike.objects.create(
                    user=self.context["user"],
                    comment=self.validated_data["comment"],
                )


class UpdateCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentLike
        fields = ("id", "comment")


class BookmarkSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = models.Bookmark
        exclude = ("user",)


class AddBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookmark
        fields = ("id", "post")

    def save(self, **kwargs):
        with transaction.atomic():
            self.instance = models.Bookmark.objects.filter(
                user=self.context["user"], post=self.validated_data["post"]
            ).first()
            if self.instance is None:
                return models.Bookmark.objects.create(
                    user=self.context["user"], post=self.validated_data["post"]
                )


class UpdateBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookmark
        fields = ("id", "post")
