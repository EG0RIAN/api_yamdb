from rest_framework import viewsets, filters, mixins

from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre
from api.permissions import AnonymReadOnlyAdminOther


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AnonymReadOnlyAdminOther,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AnonymReadOnlyAdminOther,)
    search_fields = ('name',)
