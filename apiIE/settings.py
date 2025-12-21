"""
Django settings for ApiU project (Django 5.2).
Configurado para:
- Cargar variables desde .env
- Usar MySQL (mysqlclient) en puerto 3307
- DRF + CORS en desarrollo
"""

from pathlib import Path
import os
from dotenv import load_dotenv  

# ===== RUTAS BASE =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== CARGA .ENV =====
# Muy importante cargarlo ANTES de leer las variables.
# Tu .env está al lado de manage.py.
load_dotenv(BASE_DIR / ".env")

# ===== SEGURIDAD / DEBUG =====
# SECRET_KEY: toma del .env (si no hay, usa un fallback inseguro solo para dev).
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-unsafe")

# DEBUG: True/False en texto desde .env; lo convertimos a bool.
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ALLOWED_HOSTS: lista separada por comas desde .env.
# Si está vacío, por comodidad en dev permitimos localhost/127.0.0.1.
_env_hosts = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
ALLOWED_HOSTS = _env_hosts or ["127.0.0.1", "localhost"]

# ===== APLICACIONES =====
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",   # Django REST Framework
    "corsheaders",      # CORS
    # Apps propias
    "IEAPI",  
]

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # <- Debe ir antes de CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apiIE.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Aquí podrías poner rutas a templates si usas HTML
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apiIE.wsgi.application"

# ===== BASE DE DATOS (MySQL) =====
# Usamos mysqlclient; los datos se leen del .env
# DB_HOST=localhost, DB_PORT=3307 según tu caso.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",  # mejor soporte emojis y todo unicode
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",  # valida datos
        },
        "CONN_MAX_AGE": 60,  # mantiene conexiones abiertas (mejor perf en dev)
    }
}

# ===== VALIDADORES DE PASSWORD =====
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===== I18N / TZ =====
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# ===== ARCHIVOS ESTÁTICOS =====
STATIC_URL = "static/"

# ===== PK por defecto =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== DRF =====
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ===== CORS =====
# En desarrollo, lo más simple es permitir todo:
CORS_ALLOW_ALL_ORIGINS = True
# Si prefieres restringir, comenta la línea de arriba y usa:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]