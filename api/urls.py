from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from . import views
from user.views import UserViewSet


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('genres', views.GenreViewSet, basename='genre')
router.register('titles', views.TitleViewSet, basename='title')

v1_patterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('', include(router.urls))
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
