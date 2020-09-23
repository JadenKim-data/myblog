from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"posts/(?P<post_pk>\d+)/comments", views.CommentViewSet)
router.register("categories", views.CategoryViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/posts/", views.post_list_create, name='posts-list'),
    path("api/posts/<int:pk>/", views.post_retrieve_update_delete, name='posts-detail'),
    path("api/posts/<str:category_title>/", views.PostListFilteredByCategoryAPIView.as_view()),
]
