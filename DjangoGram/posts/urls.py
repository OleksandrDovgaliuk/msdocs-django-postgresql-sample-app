from django.urls import path

from .views import HomePageView, CreatePostView, like_post, dislike_post

urlpatterns = [
    path('', HomePageView.as_view(), name="posts"),
    path('create/', CreatePostView.as_view(), name='post_create'),
    path('like_post/<int:pk>/', like_post, name='like_post'),
    path('dislike_post/<int:pk>', dislike_post, name='dislike_post')
]
