from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    '''Модель типа произведения.'''
    name = models.CharField(
        max_length=256,
        verbose_name='название категории',
        help_text='введите название категории'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='слаг категории',
        help_text='введите слаг категории'
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    '''Модель жанров.'''
    name = models.CharField(
        max_length=256,
        verbose_name='название жанра',
        help_text='ведите название жанра'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='слаг жанра',
        help_text='введите слаг жанра'
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    '''Модель произведения.'''
    name = models.CharField(
        max_length=256,
        verbose_name='название произведения',
        help_text='введите название рпоизведения'
    )
    year = models.IntegerField(
        verbose_name='год производства',
        help_text='введите год издания'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='описание произведения',
        help_text='введите описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр произведения',
        help_text='введите жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='тип произведения',
        help_text='введите тип произведения'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    '''Модель отзывов'''
    text = models.TextField(
        help_text='введите текст отзыва',
        verbose_name='текст отзыва',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='оценка произведения',
        help_text='поставьте оценку произведению'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата отзыва',
        help_text='введите дату отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор отзыва',
        help_text='укажите автора'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение с отзывом',
        help_text='введите название произведения'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
