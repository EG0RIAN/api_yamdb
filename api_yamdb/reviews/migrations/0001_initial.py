# Generated by Django 3.2 on 2023-03-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='введите название категории', max_length=256, verbose_name='название категории')),
                ('slug', models.SlugField(help_text='введите слаг категории', unique=True, verbose_name='слаг категории')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='ведите название жанра', max_length=256, verbose_name='название жанра')),
                ('slug', models.SlugField(help_text='введите слаг жанра', unique=True, verbose_name='слаг жанра')),
            ],
        ),
    ]
