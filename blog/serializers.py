import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Tag, Category

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField('avatar_url_field')
    def avatar_url_field(self, author):
        if author.avatar_url:
            if re.match(r"^https?://", author.avatar_url):
                return author.avatar_url
            if 'request' in self.context:
                host = self.context['request'].get_host()
                return "https://" + host + author.avatar_url
        else:
            return ""

    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'avatar_url', 'name']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    is_like = serializers.SerializerMethodField('is_like_field')

    def is_like_field(self, post):
        if 'request' in self.context:
            user = self.context['request'].user
            return post.like_user_set.filter(pk=user.pk).exists()
        return False

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'photo', 'post_category',
                  'tag_list', 'is_like', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']










