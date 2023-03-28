from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet, TitleViewSet

app_name = 'api'

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
