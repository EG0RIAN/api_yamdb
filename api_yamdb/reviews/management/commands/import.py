import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import (GenreTitle, Category, Genre, Title, User,
                            Review, Comment)

from api_yamdb.settings import CSV_FILES_DIR


def read_csv(path):
    try:
        with open(path, encoding='utf-8') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        print('Файл не найден.')


def read_category(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        Category(
            id=data[0],
            name=data[1],
            slug=data[2]
        ).save()


def read_genre(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        Genre(
            id=data[0],
            name=data[1],
            slug=data[2]
        ).save()


def read_titles(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        Title(
            id=data[0],
            name=data[1],
            year=data[2],
            category=Category.objects.get(id=data[3])
        ).save()


def read_genre_titles(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        GenreTitle(
            id=data[0],
            title_id=Title.objects.get(id=data[1]).id,
            genre_id=Genre.objects.get(id=data[2]).id
        ).save()


def read_users(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        User(
            id=data[0],
            username=data[1],
            email=data[2],
            role=data[3],
            bio=data[4],
            first_name=data[5],
            last_name=data[6],
        ).save()


def read_comments(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        review_id = Review.objects.get(id=data[1])
        author = User.objects.get(id=data[3])
        Comment(
            id=data[0],
            review=review_id,
            text=data[2],
            author=author,
            pub_date=data[4]
        ).save()


def read_reviews(incoming_data):
    data_without_title = incoming_data[1:]
    for data in data_without_title:
        Review(
            id=data[0],
            title_id=Title.objects.get(id=data[1]).id,
            text=data[2],
            author=User.objects.get(id=data[3]),
            score=data[4],
            pub_date=data[5],
        ).save()


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            type=str,
            help='Введите название файла для импорта'
        )


name_func = {
    'category.csv': read_category,
    'genre.csv': read_genre,
    'titles.csv': read_titles,
    'genre_title.csv': read_genre_titles,
    'users.csv': read_users,
    'review.csv': read_reviews,
    'comments.csv': read_comments
}


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            type=str,
            help='Введите название файла для импорта'
        )

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        path = os.path.join(CSV_FILES_DIR, name)
        file_data = read_csv(path)
        for func, func_name in name_func.items():
            if name == func:
                func_name(file_data)
