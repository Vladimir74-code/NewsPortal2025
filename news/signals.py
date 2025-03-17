from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import News

@receiver(post_save, sender=News)
def send_new_article_email(sender, instance, created, **kwargs):
    if created:
        for category in instance.categories.all():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                subject = f'Новая статья в категории {category.name}'
                link = f"http://127.0.0.1:8000{reverse('news:news_detail', args=[instance.id])}"
                message = f'Новая статья: {instance.title}\nКраткое содержание: {instance.content[:100]}...\nЧитать полностью: {link}'
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # Используем значение из settings.py
                    [subscriber.email],
                    fail_silently=False,  # Логируем ошибки вместо игнорирования
                )

