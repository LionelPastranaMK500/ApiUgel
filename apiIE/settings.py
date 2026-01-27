"""
Django settings for apiIE project.
Metodología Fasética (MEFH) - Versión Inmutable.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ===== RUTAS BASE =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== CARGA .ENV =====
load_dotenv(BASE_DIR / ".env")

# ===== SEGURIDAD =====
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-mounstro-dev-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Permite localhost y 127.0.0.1 por defecto, o lo que venga del .env
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# ===== APLICACIONES =====
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    # App Principal - El corazón del sistema
    "IEAPI",
]

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Indispensable para conectar con React/Vue
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apiIE.urls"

# ===== BASE DE DATOS (MySQL) =====
# Optimizada para mysqlclient y puerto 3307
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "ie_db"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3307"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "CONN_MAX_AGE": 600, # Mantener conexiones 10 min (mejor perf en dev/prod)
    }
}

# ===== LOCALIZACIÓN (Contexto Perú) =====
# Importante para que las fechas de asistencia y pagos salgan bien
LANGUAGE_CODE = "es-pe" 
TIME_ZONE = "America/Lima" 
USE_I18N = True
USE_TZ = True

# ===== DRF (Configuración Global) =====
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    # Aquí es donde más adelante meteremos los permisos por Roles
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ===== CORS =====
# En desarrollo permitimos todo, pero ya dejamos la estructura para cerrar el grifo después
CORS_ALLOW_ALL_ORIGINS = DEBUG 
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
    ]

# ===== ARCHIVOS ESTÁTICOS Y MEDIA =====
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Importante para fotos de perfil o documentos de alumnos
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===== CONFIGURACIÓN DE TEMPLATES =====
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Buscamos la carpeta templates dentro de tu app IEAPI
        "DIRS": [BASE_DIR / "IEAPI" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]