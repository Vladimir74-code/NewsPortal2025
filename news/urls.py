from django.urls import path
from . import views
from .views import NewsCreateView, ArticleCreateView, NewsUpdateView, NewsDeleteView, AuthorProfileUpdateView

app_name = 'news'

urlpatterns = [
    # Главная страница и поиск
    path('', views.news_list, name='news_list'),
    path('about/', views.about, name='about'),
    path('search/', views.news_search, name='news_search'),

    # Детальная страница новости
    path('news/<int:pk>/', views.news_detail, name='news_detail'),

    # Создание, редактирование и удаление новостей и статей
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', NewsUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', NewsDeleteView.as_view(), name='article_delete'),

    # Профиль и авторство
    path('profile/edit/', AuthorProfileUpdateView.as_view(), name='profile_edit'),
    path('become-author/', views.become_author, name='become_author'),

    # Категории и подписка
    path('category/<int:category_id>/', views.category_news, name='category_news'),
    path('category/<int:category_id>/subscribe/', views.subscribe_to_category, name='subscribe_to_category'),
    path('category/<int:category_id>/unsubscribe/', views.unsubscribe_from_category, name='unsubscribe_from_category'),
]
