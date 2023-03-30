from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

from reviews.models import Category, Genre, Title
from reviews.models import Review

# from .filters import TitlesFilter
from .permissions import (IsAuthorAdminSuperuserOrReadOnlyPermission,
                          AnonimReadOnlyPermission,
                          IsSuperUserOrIsAdminOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer,
                          SignUpSerializer, TitleSerializer, TokenSerializer,
                          TitleGETSerializer)


CustomUser = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TokenViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Выдача токена user"""
    serializer_class = TokenSerializer
    permissions_class = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """JWT token по коду подтверждения."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        user = get_object_or_404(CustomUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Регистрация нового юзера и отправка письма на почту"""
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all()
    permissions_class = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создание пользователя И Отправка письма с кодом"""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = CustomUser.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError:
            return Response(
                'Такой логин или email уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.YAMDB_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        """Возможность получения Пользователя данных о себе
        GET и PATCH запросы"""
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_class = (IsAdminUserOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_class = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorAdminSuperuserOrReadOnlyPermission
    )

    def get_queryset(self):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ( 
        IsAuthorAdminSuperuserOrReadOnlyPermission,
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=pk)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AnonimReadOnlyPermission | IsSuperUserOrIsAdminOnly)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
