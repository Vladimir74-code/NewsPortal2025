from django.contrib import admin
from .models import News, Category, Author, NewsCategory, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):  # Переименовал для консистентности
    list_display = ['title', 'short_content', 'published_date', 'author']
    list_filter = ['published_date', 'author']

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # Отображаем название категории
    list_filter = ['name']   # Фильтр по названию

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['authorUser', 'ratingAuthor']
    list_filter = ['authorUser']

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['news', 'category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['commentUser', 'commentPost', 'dateCreation', 'rating']
    list_filter = ['dateCreation', 'commentUser']