# Generated by Django 4.2 on 2024-05-15 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MediaSite', '0003_remove_actor_description_en_remove_actor_name_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='actor',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/actors/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='static/movies/', verbose_name='Постер'),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Смена',
                'verbose_name_plural': 'Смены',
            },
        ),
    ]