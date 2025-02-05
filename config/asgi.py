"""
ASGI config for your_project_name project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Устанавливаем настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# Получаем ASGI-приложение для обработки запросов
application = get_asgi_application()
