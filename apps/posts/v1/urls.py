from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.posts import views

router = DefaultRouter()

router.register("posts", views.PostViewSet, basename="post")
router.register("feed", views.FeedViewSet, basename="feed")
# router.register("post/like", views.PostLikeViewSet, basename="post-like")
router.register("post/comment", views.PostCommentViewSet, basename="post-comment")

urlpatterns = router.urls

urlpatterns += [
    path("post/like", views.PostLikeAPIView.as_view(), name='post-like')
]
