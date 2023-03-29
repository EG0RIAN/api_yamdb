from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleGETSerializer)
from reviews.models import Category, Genre, Title
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
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AnonymReadOnlyAdminOther,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AnonymReadOnlyAdminOther,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
