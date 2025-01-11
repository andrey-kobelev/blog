from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post, 'comments': comments, 'form': form},
    )


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{data['name']}\'s comments: {data['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[data['to']],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request=request,
        template_name='blog/post/share.html',
        context={'post': post, 'form': form, 'sent': sent},
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request=request,
        template_name='blog/post/comment.html',
        context={'post': post, 'form': form, 'comment': comment},
    )
