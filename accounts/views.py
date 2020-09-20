from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .permissions import UserPermission


class CreateRetrieveUpdateDestroyViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserCreateRetrieveUpdateDestroyViewSet(CreateRetrieveUpdateDestroyViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


