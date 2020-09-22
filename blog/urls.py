from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("posts", views.PostViewSet)
router.register(r"posts/(?P<post_pk>\d+)/comments", views.CommentViewSet)
router.register("categories", views.CategoryViewSet)


urlpatterns = [
    re_path(r"^posts/(?P<category_title>[a-zA-Zㄱ-힣]+)/$", views.PostListFilteredByCategoryAPIView.as_view()),   #TODO: api/안에 모든 뷰가 포함되도록 작성 필요
    path("api/", include(router.urls))
]
