from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']

    # Автоматически преобразует поле title в slug.
    prepopulated_fields = {'slug': ('title',)}

    # При создании поста, в поле автора не будут всплывать все авторы,
    # а откроется отдельное окно с авторами. Выбрав автора, в поле попадет его id.
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
