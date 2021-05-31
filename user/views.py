from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    # permission_classes = [IsAdminUser]
    search_fields = ['user__username', ]
