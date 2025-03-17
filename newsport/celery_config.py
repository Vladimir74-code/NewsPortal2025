import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsport.settings')

# Создание экземпляра приложения Celery
app = Celery('newsport')

# Загрузка конфигурации из settings.py (с префиксом CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в файлах tasks.py
app.autodiscover_tasks()

# Расписание задач
app.conf.beat_schedule = {
    'send-weekly-digest': {  # Имя задачи в расписании
        'task': 'news.tasks.send_weekly_digest',  # Полный путь к задаче
        'schedule': crontab(minute='*/1'),  # Понедельник, 8:00
    },
}