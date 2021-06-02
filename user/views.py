import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api import permissions

from .serializers import (ConfirmationCodeAndEmailSerializer, EmailSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAdmin]
    search_fields = ['user__username', ]


class CurrentUserDetail(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response('Авторизуйтесь, пожалуйста',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user, data=request.data,
                                        partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Авторизуйтесь, пожалуйста',
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_view(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            return Response('Вы уже зарегистрированы',
                            status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = random.randint(100000, 999999)
        username = email.split('@')[0]
        message = f'Ваш код подтверждения:{confirmation_code}'
        User.objects.create_user(email=email,
                                 confirmation_code=confirmation_code,
                                 username=username, password=confirmation_code)
        send_mail('Код подтверждения', message,
                  settings.DEFAULT_FROM_EMAIL, [email])
        return Response('Код отправлен', status=status.HTTP_200_OK)
    return Response('Email указан неверно', status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_view(request):
    serializer = ConfirmationCodeAndEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        refresh = get_tokens_for_user(user)
        return Response(refresh, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
