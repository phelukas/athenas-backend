from .base import *
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default="seusite.com,www.seusite.com", cast=Csv()
)

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="athenas-prod"),
        "USER": config("DB_USER", default="seu_usuario_prod"),
        "PASSWORD": config("DB_PASSWORD", default="sua_senha_prod"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}
