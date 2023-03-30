from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                       GenreViewSet, ReviewViewSet, SignUpViewSet,
                       TitleViewSet, TokenViewSet)

app_name = 'api'

router = DefaultRouter()
router_v1_auth = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router_v1_auth.register('signup', SignUpViewSet, basename='signup')
router_v1_auth.register('token', TokenViewSet, basename='token')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/', include(router_v1_auth.urls)),
    path('v1/', include(router.urls)),
]
