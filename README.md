NewsPortal2025
Это мой учебный проект новостного портала, который я разрабатываю на Django. Проект включает авторизацию через django-allauth, фильтрацию новостей, отправку email и задачи Celery. Здесь я описываю задание по настройке логирования, которое я выполнил для ментора.
Задание: Настройка логирования
Цель: Настроить систему логирования для проекта, чтобы отслеживать события, ошибки и действия пользователей. Логи должны писаться в консоль, файлы и отправляться на почту в зависимости от уровня и типа событий.
Что нужно было сделать:

Выводить в консоль все логи уровня DEBUG и выше, когда DEBUG = True. Для WARNING и выше добавлять путь к файлу, а для ERROR — стек вызовов.
Писать логи уровня INFO и выше в файл general.log, но только когда DEBUG = False.
Сохранять ошибки (ERROR и выше) для django.request, django.server, django.template, django.db.backends в файл errors.log.
Логировать события безопасности (django.security, уровень INFO и выше) в файл security.log.
Отправлять ошибки django.request и django.server на почту администратору, когда DEBUG = False.

Как я это сделал:

В файле newsport/settings.py я настроил секцию LOGGING. Использовал словари для форматтеров, хэндлеров и логгеров, как в документации Django.
Создал кастомный класс ConsoleFormatter, который меняет формат логов в консоли: для WARNING и выше добавляет путь к файлу (pathname), а для ERROR — информацию об исключении (exc_info).
Настроил фильтры DebugTrueFilter и DebugFalseFilter, чтобы разделять логирование для DEBUG = True (консоль) и DEBUG = False (файлы и почта).
Указал пути для файлов логов в папке logs/ (автоматически создаётся, если её нет). Использовал RotatingFileHandler с лимитом 5 МБ и 5 резервных копий.
Подключил AdminEmailHandler для отправки ошибок на почту через SMTP Яндекса. Настроил EMAIL_HOST_PASSWORD через python-decouple и файл .env для безопасности.
Добавил .env, logs/, *.log и db.sqlite3 в .gitignore, чтобы не загружать их на GitHub.

Проблемы и решения:

Сначала был ValueError из-за неправильного форматтера (CallbackFormatter). Я заменил его на кастомный ConsoleFormatter, и ошибка исчезла.
Были конфликты при слиянии с GitHub, особенно в settings.py. Я разрешил их, выбрав версию с python-decouple и ACCOUNT_LOGIN_METHODS.
Научился использовать git-filter-repo, чтобы удалить старый SECRET_KEY и EMAIL_HOST_PASSWORD из истории репозитория, так как они были в публичном доступе.

Результат:

Логирование работает! При DEBUG = True все логи от DEBUG выводятся в консоль PyCharm. Например: 2025-05-31 12:24:18 [DEBUG] Waiting for apps ready_event.
При DEBUG = False логи пишутся в logs/general.log, ошибки — в logs/errors.log, а события безопасности — в logs/security.log.
Ошибки django.request и django.server готовы отправляться на почту (проверял с EMAIL_BACKEND = 'console.EmailBackend').
Все изменения загружены на GitHub (https://github.com/Vladimir74-code/NewsPortal2025), чувствительные данные удалены из истории.

Как проверить:

Клонируйте репозиторий: git clone https://github.com/Vladimir74-code/NewsPortal2025.git.
Установите зависимости: pip install -r requirements.txt.
Создайте файл .env с SECRET_KEY и EMAIL_HOST_PASSWORD.
Запустите сервер: python manage.py runserver.
Откройте http://127.0.0.1:8000/news/ и проверьте консоль для логов.
Переключите DEBUG = False в settings.py и проверьте файлы в папке logs/.

Проблемы с Gidhub, возникли потому что я с семьей уехал в отпуск и работал с ноутбука!!! спасибо и добра!! 😊
