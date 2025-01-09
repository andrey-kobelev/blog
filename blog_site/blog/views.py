from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    paginator = Paginator(
        object_list=Post.published.all(),
        per_page=settings.PAGINATION,
    )
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(number=page)
    except PageNotAnInteger:
        posts = paginator.page(number=1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='blog/post/list.html',
        context={'posts': posts},
    )


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
