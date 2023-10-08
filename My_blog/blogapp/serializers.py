from django.db import transaction
from django.db.models import Count
from rest_framework import serializers

from My_blog.blogapp import models
from My_blog.userapp.serializers import UserDataSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestNotification
        fields = "__all__"


class Base(serializers.Serializer):
    class Meta:
        abstract = True

    def booked(self, obj):
        return obj.id in models.Bookmark.objects.filter(
            user=self.context.get("user")
        ).values_list("post", flat=True)

    def like(self, obj):
        return obj.id in models.PostLike.objects.filter(
            user=self.context.get("user")
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

    def commentlike(self, obj):
        return obj.id in models.CommentLike.objects.filter(
            user=self.context.get("user")
        ).values_list("comment", flat=True)

    def commentlikecount(self, obj):
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

    def get_date(self, obj):
        return obj.date.strftime("%d %b %Y")


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


class BlogDetailedSerializer(serializers.ModelSerializer, Base):
    related_blogs = BlogDataSerializer(many=True)
    category = BlogCategoryDataSerializer()
    date = serializers.SerializerMethodField()
    created_by = UserDataSerializer()

    class Meta:
        model = models.Blog
        exclude = ("slug",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer, Base):
    date = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField(method_name="booked")
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")

    class Meta:
        model = models.Post
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer, Base):
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


class PostDetailedSerializer(serializers.ModelSerializer, Base):
    blog = BlogDataSerializer()
    user = UserDataSerializer(read_only=True)
    tags = TagSerializer(many=True)
    date = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField(method_name="booked")
    is_liked = serializers.SerializerMethodField(method_name="like")
    likes = serializers.SerializerMethodField(method_name="likecount")
    comments = serializers.SerializerMethodField(method_name="postcomments")

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
                    user=self.context["user"], post=self.validated_data["post"]
                )


class UpdatePostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ("id", "post")


class CommentSerializer(serializers.ModelSerializer, Base):
    date = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField(method_name="commentlike")
    likes = serializers.SerializerMethodField(method_name="commentlikecount")

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "user",
            "post",
            "text",
            "picture",
            "date",
            "is_liked",
            "likes",
        )


class CommentDetailedSerializer(serializers.ModelSerializer, Base):
    date = serializers.SerializerMethodField()
    post = PostSerializer()
    is_liked = serializers.SerializerMethodField(method_name="commentlike")
    likes = serializers.SerializerMethodField(method_name="commentlikecount")

    class Meta:
        model = models.Comment
        exclude = ("user",)


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
