from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import GenreViewSet, CategoryViewSet, TitleViewSet

app_name = 'api'

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
