# Generated by Django 5.0 on 2024-01-29 09:15

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name='Возраст')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='actors/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Актеры и режиссеры',
                'verbose_name_plural': 'Актеры и режиссеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('slug', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('slug', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(-1, 'Не нравится'), (1, 'Нравится')], verbose_name='Голос')),
                ('user_ip', models.CharField(default=0, max_length=15, verbose_name='IP адрес')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Лайк & Дизлайк',
                'verbose_name_plural': 'Лайки & Дизлайки',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('tagline', models.CharField(blank=True, default='', max_length=100, verbose_name='Слоган')),
                ('kinopoisk_id', models.IntegerField(default=0, unique=True, verbose_name='Кинопоиск ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('poster', models.ImageField(upload_to='movies/', verbose_name='Постер')),
                ('year', models.PositiveSmallIntegerField(default=2019, verbose_name='Дата выхода')),
                ('country', models.CharField(max_length=30, verbose_name='Страна')),
                ('world_premiere', models.DateField(default=datetime.date.today, verbose_name='Премьера в мире')),
                ('budget', models.PositiveIntegerField(blank=True, default=0, help_text='сумма в долларах', verbose_name='Бюджет')),
                ('kinopoisk_rating', models.FloatField(default=0, verbose_name='Рейтинг Кинопоиск')),
                ('running_time', models.FloatField(default=0, verbose_name='Продолжительность')),
                ('fess_in_world', models.PositiveIntegerField(blank=True, default=0, help_text='сумма в долларах', verbose_name='Сборы в мире')),
                ('slug', models.SlugField(max_length=130, unique=True)),
                ('draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('actors', models.ManyToManyField(related_name='film_actor', to='MediaSite.actor', verbose_name='актеры')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MediaSite.category', verbose_name='Категория')),
                ('directors', models.ManyToManyField(related_name='film_director', to='MediaSite.actor', verbose_name='режиссер')),
                ('genres', models.ManyToManyField(to='MediaSite.genre', verbose_name='жанры')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='MovieShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='movie_shots/', verbose_name='Изображение')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MediaSite.movie', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'Кадр из фильма',
                'verbose_name_plural': 'Кадры из фильма',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_reviews', models.IntegerField(default=0, verbose_name='Кол-во оценок')),
                ('sum_rating', models.BigIntegerField(default=0, verbose_name='Кол-во звезд')),
                ('avg_rating', models.FloatField(default=0, verbose_name='Средняя оценка')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='MediaSite.movie', verbose_name='фильм')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default=0, max_length=15, verbose_name='IP адрес')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('rating', models.IntegerField(blank=True, default=0, verbose_name='Оценка пользователя')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='MediaSite.movie', verbose_name='фильм')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='MediaSite.reviews', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]