from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class RetrieveUpdateDestroyViewSet(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    pass

class UserCreateAPIView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserRetrieveUpdateDestroyViewSet(RetrieveUpdateDestroyViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

