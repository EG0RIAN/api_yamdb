from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Category, Genre, Title
from .models import Comment, Review
# поменять на модели    

CustomUser = get_user_model()


class TokenSerializer(serializers.Serializer):
    """Сериализатор для выдачи пользователю Токена"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        fields = ('username', 'email', )

    def validate(self, data):
        """Запрет на имя me, А так же Уникальность полей username и email"""
        if data.get('username').lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', )
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context[
            'request'].parser_context['kwargs'].get('title_id')
        author = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if 1 > value > 10:
            raise serializers.ValidationError('Недопустимое значение!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Для Комментариев"""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Для Категорий"""
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Для жанров"""
    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Для произведений"""

    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор Для чтения произведений """
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
