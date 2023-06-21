from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse

from DjangoGram.posts.forms import PostForm
from DjangoGram.posts.models import Post


class HomePageView(ListView):
    model = Post
    template_name = "posts_list.html"


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        post.likes.add(request.user)
        return redirect('/posts', pk=pk)
    else:
        return redirect('login')  # replace 'login' with the name of your login view


@require_POST
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        post.likes.remove(request.user)
        return redirect('/posts', pk=pk)
    else:
        return redirect('login')
