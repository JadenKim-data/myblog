from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from . import views

router = DefaultRouter()
router.register("users", views.UserCreateRetrieveUpdateDestroyViewSet)

urlpatterns = [
    # path('signup/', views.SignupAPIView.as_view(), name="signup"),
    path('api/token/', obtain_jwt_token),
    # path('api/users/', views.UserCreateAPIView.as_view()),
    path('api/', include(router.urls)),
]