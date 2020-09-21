from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
# from imagekit.models import ProcessedImageField
# from imagekit.processors import Thumbnail


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(TimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="my_post_list",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    # thumbnail = ProcessedImageField(
    #     upload_to="blog/post/thumbnail/%Y/%m/%d",
    #     processors=[Thumbnail(120, 120)],
    #     format="JPEG",
    #     options={'quality': 60},
    #     blank=True
    # ) PilKit에서 processor목록을 확인 가능
    photo = models.ImageField(upload_to="blog/post/photo/%Y/%m/%d", blank=True)
    post_category = TreeForeignKey(
        'Category',
        related_name="category_post_list",
        on_delete=models.SET_NULL,
        null=True,
    )
    tag_list = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='tag_post_list'
    )
    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="like_post_list"
    )

    class Meta:
        ordering = ['-id']


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tree_id', 'lft']

    class MPTTMeta:
        ordering_insertion_by = ['title']

    def __str__(self):
        return self.title


class Tag(TimeStampedModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Comment(TimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_comment_list"
    )
    comment_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_comment_list"
    )
    message = models.CharField(max_length=1000)
    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="like_comment_list"
    )
