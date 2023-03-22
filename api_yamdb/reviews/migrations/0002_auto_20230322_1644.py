# Generated by Django 3.2 on 2023-03-22 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='введите название рпоизведения', max_length=256, verbose_name='название произведения')),
                ('year', models.IntegerField(help_text='введите год издания', verbose_name='год производства')),
                ('description', models.TextField(blank=True, help_text='введите описание произведения', null=True, verbose_name='описание произведения')),
                ('category', models.ForeignKey(blank=True, help_text='введите тип произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='тип произведения')),
                ('genre', models.ManyToManyField(help_text='введите жанр произведения', related_name='title', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='жанр произведения')),
            ],
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='reviews.title'),
        ),
    ]
