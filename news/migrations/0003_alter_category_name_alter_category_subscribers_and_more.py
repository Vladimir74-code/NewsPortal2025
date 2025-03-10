# Generated by Django 5.1.5 on 2025-03-05 04:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_subscribers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_categories', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики'),
        ),
        migrations.AlterField(
            model_name='news',
            name='categories',
            field=models.ManyToManyField(blank=True, through='news.NewsCategory', to='news.category', verbose_name='Категории'),
        ),
    ]
