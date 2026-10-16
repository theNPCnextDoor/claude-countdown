from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "dev-only-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth", "solver"]
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "config.urls"
DATABASES = {}  # aucune base de données nécessaire
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
