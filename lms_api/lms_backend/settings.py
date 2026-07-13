"""Cấu hình trung tâm của dự án LMS."""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# =========================================================
# Đường dẫn và biến môi trường
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env.local")


# =========================================================
# Cấu hình bảo mật cơ bản
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "",
).split(",")


# =========================================================
# Ứng dụng
# =========================================================

INSTALLED_APPS = [
    # Ứng dụng mặc định của Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Thư viện bên thứ ba
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # Ứng dụng của dự án
    "users",
    "courses",
    "enrollments",
    "common",
    "assessments",
    "reviews",
    "analytics",
    "chat",
    "rag",
]


# =========================================================
# Middleware
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL và template
# =========================================================

ROOT_URLCONF = "lms_backend.urls"

TEMPLATES = [
    {
        "BACKEND": ("django.template.backends.django." "DjangoTemplates"),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                ("django.template.context_processors." "debug"),
                ("django.template.context_processors." "request"),
                ("django.contrib.auth.context_processors." "auth"),
                ("django.contrib.messages.context_processors." "messages"),
            ],
        },
    },
]

WSGI_APPLICATION = "lms_backend.wsgi.application"


# =========================================================
# Cơ sở dữ liệu
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "OPTIONS": {
            "ssl": {
                "ca": str(BASE_DIR / "cert" / "ca.pem"),
            },
        },
    },
}


# =========================================================
# Kiểm tra mật khẩu
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]


# =========================================================
# Ngôn ngữ và múi giờ
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =========================================================
# Static và media
# =========================================================

STATIC_URL = "static/"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# Cấu hình Django chung
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"


# =========================================================
# Django REST Framework
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        ("rest_framework_simplejwt.authentication." "JWTAuthentication"),
        ("rest_framework.authentication." "SessionAuthentication"),
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": ("rest_framework.pagination." "PageNumberPagination"),
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}


# =========================================================
# CORS
# =========================================================

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True


# =========================================================
# Simple JWT
# =========================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}


# =========================================================
# Logging
# =========================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": ("{levelname} {asctime} " "{module} {message}"),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


RAG_CHROMA_PATH = os.getenv(
    "RAG_CHROMA_PATH",
    str(BASE_DIR / "chroma_db"),
)

RAG_COLLECTION_NAME = os.getenv(
    "RAG_COLLECTION_NAME",
    "lms_user_documents",
)

RAG_OLLAMA_BASE_URL = os.getenv(
    "RAG_OLLAMA_BASE_URL",
    "http://localhost:11434",
)

RAG_LLM_MODEL = os.getenv(
    "RAG_LLM_MODEL",
    "qwen2.5:3b",
)

RAG_EMBED_MODEL = os.getenv(
    "RAG_EMBED_MODEL",
    "bge-m3:latest",
)

RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1000"))

RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "180"))

RAG_TOP_K = int(os.getenv("RAG_TOP_K", "6"))

RAG_MAX_DISTANCE = float(os.getenv("RAG_MAX_DISTANCE", "0.82"))

RAG_MAX_FILE_SIZE_MB = int(os.getenv("RAG_MAX_FILE_SIZE_MB", "30"))

RAG_OLLAMA_TIMEOUT = float(os.getenv("RAG_OLLAMA_TIMEOUT", "180"))

RAG_ALLOWED_EXTENSIONS = [
    "pdf",
    "txt",
    "docx",
    "pptx",
]
