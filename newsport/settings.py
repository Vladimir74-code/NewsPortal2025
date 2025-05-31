"""
Django settings for NewsPortal2025 project.
"""

from pathlib import Path
import os
import logging
from django.conf import settings
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_filters',
    'news.apps.NewsConfig',  # Приложение news
    'django_celery_beat',  # Для управления расписанием Celery
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Настройки django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Обязательная верификация
ACCOUNT_EMAIL_REQUIRED = True  # Email обязателен
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_REDIRECT_URL = '/news/'
LOGIN_REDIRECT_URL = '/news/'
LOGOUT_REDIRECT_URL = '/news/'
LOGIN_URL = '/accounts/login/'

ROOT_URLCONF = 'newsport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Для общих шаблонов (например, base.html)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsport.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'  # Синхронизировано с Celery
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки отправки email через SMTP Яндекса
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'budkeevvladimir32@yandex.ru'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'NewsPortal <budkeevvladimir32@yandex.ru>'
ADMINS = [('Admin', 'budkeevvladimir32@yandex.ru')]  # Для отправки ошибок на почту

# Настройки Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis как брокер
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis для хранения результатов
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'  # Часовой пояс
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 минут на выполнение задачи

# Конфигурация логирования для NewsPortal2025
# - Консоль: DEBUG+ при DEBUG=True (включает pathname для WARNING+, exc_info для ERROR+)
# - general.log: INFO+ при DEBUG=False (время, уровень, модуль, сообщение)
# - errors.log: ERROR+ для django.request, django.server, django.template, django.db.backends
# - security.log: INFO+ для django.security
# - Почта: ERROR+ для django.request, django.server при DEBUG=False

# Кастомный форматтер для консоли
class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.WARNING:
            self._style._fmt = '%(asctime)s [%(levelname)s] %(message)s (%(pathname)s)'
        else:
            self._style._fmt = '%(asctime)s [%(levelname)s] %(message)s'

        if record.levelno >= logging.ERROR and record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        else:
            record.exc_text = None

        return super().format(record)

# Кастомные фильтры
class DebugTrueFilter(logging.Filter):
    def filter(self, record):
        return settings.DEBUG

class DebugFalseFilter(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG

# Путь к файлам логов (относительно BASE_DIR)
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)  # exist_ok=True для избежания ошибок при повторном создании

# Конфигурация логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'debug_true': {
            '()': DebugTrueFilter,
        },
        'debug_false': {
            '()': DebugFalseFilter,
        },
    },
    'formatters': {
        'console_formatter': {
            '()': ConsoleFormatter,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'general_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'errors_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(message)s %(pathname)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'security_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'email_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(message)s %(pathname)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['debug_true'],
            'formatter': 'console_formatter',
            'level': 'DEBUG',
        },
        'general_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'general.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filters': ['debug_false'],
            'formatter': 'general_formatter',
            'level': 'INFO',
            'delay': True,
        },
        'errors_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'errors_formatter',
            'level': 'ERROR',
            'delay': True,
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'security_formatter',
            'level': 'INFO',
            'delay': True,
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['debug_false'],
            'formatter': 'email_formatter',
            'level': 'ERROR',
            'include_html': False,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'general_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Отладка для email (временный консольный бэкенд, если SMTP не работает)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Отладка
import logging
logging.basicConfig(level=logging.DEBUG)