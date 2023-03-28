import csv

from django.core.management.base import BaseCommand
from reviews.models import GenreTitle, Category, Genre, Title


def read_csv(path):
    try:
        with open(path, encoding='utf-8') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        print('Файл не найден.')


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
        path = '../api_yamdb/static/data/' + name
        file_data = read_csv(path)
        data_without_title = file_data[1:]
        print(data_without_title)
        if name == 'category.csv':
            for data in data_without_title:
                Category(
                    id=data[0],
                    name=data[1],
                    slug=data[2]
                ).save
        if name == 'genre.csv':
            for data in data_without_title:
                Category(
                    id=data[0],
                    name=data[1],
                    slug=data[2]
                ).save
        if name == 'genre_title.csv':
            for data in data_without_title:
                title_id = Title.objects.get(id=data[1])
                genre_id = Genre.objects.get(id=data[2])
                GenreTitle.objects.create(
                    id=data[0],
                    title_id=title_id,
                    genre_id=genre_id
                )
        if name == 'titles.csv':
            for data in data_without_title:
                category = Category.objects.get(id=data[3])
                Title(
                    id=data[0],
                    name=data[1],
                    year=data[2],
                    category=category
                ).save()
