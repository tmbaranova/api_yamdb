from django.contrib.auth import get_user_model

from rest_framework import viewsets

from api import permissions

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAdmin]
    search_fields = ['user__username', ]
