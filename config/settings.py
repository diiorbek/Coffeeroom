from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*uudoramjrrfa(j^5u@e)nlo==7$eufnsrzbte4protpo-(#@f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "https://api.sifatedu.uz",
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False  # True только для разработки
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://127.0.0.1:3000",
    "https://api.sifatedu.uz",  # Ваш основной домен
    "https://coffee-room.netlify.app",
    "https://coffee-room-shop.vercel.app",
]
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrf-token",
    "x-requested-with",
]
CORS_ALLOW_CREDENTIALS = True

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'allauth',
    'rest_framework_simplejwt.token_blacklist',
    "corsheaders",
    'common',
    'modeltranslation',
    'Coffeeroom',
    'Order',
]

ASGI_APPLICATION = 'config.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'DIRS': [],
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

AUTH_USER_MODEL = 'account.User'
WSGI_APPLICATION = 'config.wsgi.application'

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


WSGI_APPLICATION = 'config.wsgi.application'
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

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True
USE_L10N = True

USE_TZ = True

import os
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Если используется на продакшене, убедитесь, что указаны правильные пути:
STATIC_ROOT = "/home/staticfiles/"

# Если вы хотите, чтобы статика автоматически обслуживалась во время разработки
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API доставки Coffeeroom",
    "DESCRIPTION": "API документация для проекта Coffeeroom",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/",
    "SERVE_INCLUDE_SCHEMA": False,
}

JAZZMIN_SETTINGS = {
    'site_title': 'Административная панель Coffeeroom',
    'site_header': 'Административная панель Coffeeroom',
    'site_brand': 'Coffeeroom',
    'welcome_sign': 'Добро пожаловать в административную панель Coffeeroom',
    'copyright': 'Coffeeroom',
    'show_ui_builder': False,
    'show_navigation': True,
    'theme': 'dark',
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # or whatever duration you prefer
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


LANGUAGES = (
    ('ru', 'Russian'),
    ('uz', 'Uzbek'),
    ('en', 'English'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

