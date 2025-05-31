import django_filters
from .models import News
from django import forms

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(
        field_name='author__authorUser__username',  # Фильтр по имени пользователя автора
        lookup_expr='icontains',
        label='Author'
    )
    published_date = django_filters.DateFilter(
        lookup_expr='gte',
        label='Published After',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = News
        fields = ['title', 'author', 'published_date']