from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from My_blog.blogapp import models, serializers


class FollowerView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.FollowerSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Follow.objects.filter(following=self.request.user)


class FollowingView(viewsets.ModelViewSet):
    serializer_class = serializers.FollowSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Follow.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return serializers.AddFollowSerializer
        return super().get_serializer_class()


class BlogCategory(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BlogCategorySerializer
    queryset = models.BlogCategory.objects.all()
    pagination_class = None
    lookup_field = "slug"


class BlogViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("category__slug",)
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BlogDetailedSerializer
        return super().get_serializer_class()


class FeedView(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.FeedSerializer
    filterset_fields = ("blog__category__slug", "tags__name")
    pagination_class = None

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        user = self.request.user
        user_following = models.Follow.objects.filter(user=user)
        following_users = [user]
        following_users.extend(user_following.values_list("following", flat=True))
        return models.Post.objects.filter(user__in=following_users)


class PostView(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("blog__category__slug", "tags__name")
    pagination_class = None

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PostDetailedSerializer
        if self.action == "create":
            return serializers.AddPostSerializer
        if self.action == "update":
            return serializers.UpdatePostSerializer
        return serializers.PostSerializer


class TagView(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    pagination_class = None

    def get_serializer_context(self):
        return {"user": self.request.user}


class PostLikeView(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostLikeSerializer
    pagination_class = None

    def get_queryset(self):
        return models.PostLike.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddPostLikeSerializer
        if self.action == "update":
            return serializers.UpdatePostLikeSerializer
        return super().get_serializer_class()


class CommentView(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CommentDetailedSerializer
        if self.action == "create":
            return serializers.AddCommentSerializer
        if self.action == "update":
            return serializers.UpdateCommentSerializer
        return super().get_serializer_class()


class CommentLikeView(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentLikeSerializer
    pagination_class = None

    def get_queryset(self):
        return models.CommentLike.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddCommentLikeSerializer
        if self.action == "update":
            return serializers.UpdateCommentLikeSerializer
        return super().get_serializer_class()


class BookmarkView(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BookmarkSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Bookmark.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.AddBookmarkSerializer
        if self.action == "update":
            return serializers.UpdateBookmarkSerializer
        return super().get_serializer_class()
