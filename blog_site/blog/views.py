from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    """  Альтернативное представление списка постов """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = settings.PAGINATION
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post},
    )
