from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from users.serializers import CreateUserSerializer


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer