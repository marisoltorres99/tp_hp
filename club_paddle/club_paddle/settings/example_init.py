from club_paddle.settings.development import *

# Datos acceso DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "STORAGE_ENGINE": "INNODB",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "club_paddle",
        "USER": "club_paddle_user",
        "PASSWORD": "<COMPLETAR_PASSWORD>",
    }
}

# Idioma
USE_L10N = True
LANGUAGE_CODE = "es-es"
LANGUAGES = [
    ("es", "Spanish"),
]

# Zona horaria
TIME_ZONE = "America/Argentina/Buenos_Aires"

# Configuracion envio de mail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Reemplazar con dirección de correo electrónico para envíos (SMTP)
EMAIL_HOST_USER = "COMPLETAR_EMAIL"
# Reemplazar con contraseña de correo electrónico para envíos (SMTP)
EMAIL_HOST_PASSWORD = "COMPLETAR_EMAIL_PASSWORD"

# Rutas para subir archivos
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
