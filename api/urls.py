from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import CurrentUserDetail, UserViewSet, login_view, signup_view

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('genres', views.GenreViewSet, basename='genre')
router.register('titles', views.TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

v1_patterns = [
    path('auth/token/', login_view,
         name='token'),
    path('auth/token/refresh/', login_view,
         name='token_refresh'),
    path('users/me/', CurrentUserDetail.as_view()),
    path('auth/email/', signup_view, name='email'),

    path('', include(router.urls)),

]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
