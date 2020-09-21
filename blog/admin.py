from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Post, Category, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'title',
    )
    mptt_level_indent = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
