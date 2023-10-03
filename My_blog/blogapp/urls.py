from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("followers", views.FollowerView, basename="followers")
router.register("following", views.FollowingView, basename="following")
router.register("blogs", views.BlogViewset)
router.register("blog_categories", views.BlogCategory)
router.register("tags", views.TagView, basename="tags")
router.register("feed", views.FeedView, basename="feed")
router.register("my_posts", views.PostView, basename="my_posts")
router.register("post_like", views.PostLikeView, basename="post_like")
router.register("my_comments", views.CommentView, basename="my_comments")
router.register("comment_like", views.CommentLikeView, basename="comment_like")
router.register("bookmarks", views.BookmarkView, basename="bookmarks")


urlpatterns = [
    path("", include(router.urls)),
]
