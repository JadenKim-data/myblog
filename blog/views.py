from django.shortcuts import render
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post, Tag, Category, Comment
from .serializers import PostSerializer, TagSerializer, CategorySerializer, CommentSerializer


# class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     pass

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        post = self.get_object()
        post.like_user_set.add(self.request.user)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user)
        return Response(status.HTTP_204_NO_CONTENT)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(comment_post__pk=self.kwargs['post_pk'])
        return qs


class PostListFilteredByCategoryAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(post_category__title=self.kwargs['category_title'])
        return qs


# class PostListFilteredByCategoryViewSet(ListViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         qs = super().get_queryset()
#         category_title = self.kwargs['category_title']
#         if Category.objects.filter(title=category_title).exists():
#             category_pk = Category.objects.get(title=category_title).pk
#             qs = qs.filter(post_category=category_pk)
#         return qs
