from rest_framework import viewsets

from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
