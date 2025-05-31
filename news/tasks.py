from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from .models import News, Category
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_news_notification(news_id):
    try:
        news = News.objects.get(id=news_id)
        for category in news.categories.all():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                subject = f'Новая новость в категории {category.name}'
                link = f"http://127.0.0.1:8000{reverse('news:news_detail', args=[news.id])}"
                message = f'Новая новость: {news.title}\nКраткое содержание: {news.content[:100]}...\nЧитать полностью: {link}'
                send_mail(
                    subject,
                    message,
                    'budkeevvladimir32@yandex.ru',  # Замени на email из settings.py, если отличается
                    [subscriber.email],
                    fail_silently=False,
                )
    except News.DoesNotExist:
        print(f"Новость с ID {news_id} не найдена.")

@shared_task
def send_weekly_digest():
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_news = News.objects.filter(published_date__gte=one_week_ago)
    if recent_news.exists():
        for category in Category.objects.all():
            subscribers = category.subscribers.all()
            if subscribers:
                news_in_category = recent_news.filter(categories=category)
                if news_in_category.exists():
                    subject = f'Еженедельный дайджест новостей в категории {category.name}'
                    message = 'Новые новости за последнюю неделю:\n\n'
                    for news in news_in_category:
                        link = f"http://127.0.0.1:8000{reverse('news:news_detail', args=[news.id])}"
                        message += f'{news.title} - {link}\n'
                    send_mail(
                        subject,
                        message,
                        'budkeevvladimir32@yandex.ru',
                        [subscriber.email for subscriber in subscribers],
                        fail_silently=False,
                    )