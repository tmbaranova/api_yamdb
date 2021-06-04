from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import (ConfirmationCodeAndEmailSerializer,
                              EmailSerializer, UserSerializer)

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleReadSerializer)

User = get_user_model()


class OnlyForCreateDestroyListViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class CategoryViewSet(OnlyForCreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(OnlyForCreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleCreateSerializer
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('-id')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        author = self.request.user
        if Review.objects.filter(title=title, author=author).exists():
            raise exceptions.ValidationError('Only one review '
                                             'per title allowed')
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
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
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Авторизуйтесь, пожалуйста',
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        confirmation_code = user.confirmation_code
        message = f'Ваш код подтверждения:{confirmation_code}'
        send_mail('Код подтверждения', message,
                  settings.DEFAULT_FROM_EMAIL, [email])
        return Response('Код отправлен еще раз', status=status.HTTP_200_OK)

    username = email.split('@')[0]
    user = User.objects.create_user(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(email=email).update(
        confirmation_code=confirmation_code)
    message = f'Ваш код подтверждения:{confirmation_code}'
    send_mail('Код подтверждения', message,
              settings.DEFAULT_FROM_EMAIL, [email])
    return Response('Код отправлен', status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = ConfirmationCodeAndEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    user = get_object_or_404(User, email=email)
    refresh = get_tokens_for_user(user)
    return Response(refresh, status=status.HTTP_200_OK)
