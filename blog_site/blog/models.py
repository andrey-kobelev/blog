from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


TITLE_MAX_LENGTH = 250
SLUG_MAX_LENGTH = 250
STATUS_MAX_LENGTH = 2
NAME_FOR_COMMENT_MAX_LENGTH = 80


User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique_for_date='publish',
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        return reverse(
            viewname='blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(max_length=NAME_FOR_COMMENT_MAX_LENGTH)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
