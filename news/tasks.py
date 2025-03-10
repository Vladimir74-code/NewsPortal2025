from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import News, Category
from datetime import timedelta

@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(days=7)
    new_articles = News.objects.filter(published_date__gte=one_week_ago)
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        category_articles = new_articles.filter(categories=category)
        if category_articles.exists():
            for user in subscribers:
                html_content = render_to_string(
                    'weekly_newsletter.html',
                    {
                        'username': user.username,
                        'articles': category_articles,
                    }
                )
                send_mail(
                    subject=f"Еженедельный дайджест: {category.name}",
                    message=f"Здравствуй, {user.username}! Вот новые статьи за неделю.",
                    from_email=None,
                    recipient_list=[user.email],
                    html_message=html_content,
                    fail_silently=True,
                )