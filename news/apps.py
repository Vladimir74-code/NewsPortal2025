from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # Подключаем сигналы и задачи
        import news.signals  # Подключаем сигналы (если они есть)
        from news.tasks import send_weekly_digest  # Импортируем задачу с правильным именем