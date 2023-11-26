# Bajar Python 3.10 para Windows

Desde la pagina oficial de Python bajar 3.10.11 para Windows:

https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

## Para instalarlo usar las opciones

	"Install Now"

	[X] Add python.exe to PATH

# Bajar GitHub Desktop

https://central.github.com/deployments/desktop/desktop/latest/win32

## Instalar GitHub Desktop y loguearse con tu cuenta Git

Luego usar la opcion: `Clonar repositorio desde internet`, y en la `pestaña URL` ingresar la URL del repositorio, ej:

https://github.com/marisoltorres99/tp_hp.git

# Crear la DB para el proyecto web

Desde el editor MySQL Workbench (o cualquier otro editor) hacer:

```
CREATE DATABASE club_paddle DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_spanish_ci;

CREATE USER 'club_paddle_user'@'localhost' IDENTIFIED BY 'aca inventar un password';

GRANT ALL PRIVILEGES ON club_paddle.* TO 'club_paddle_user'@'localhost';
```

# Crear archivo de configuracion para el proyecto web

Crear archivo llamado `__init__.py` dentro de la ruta `tp_hp\club_paddle\club_paddle\settings\`

Y pegarle el siguiente código:


```
from .django_base import *

# datos acceso DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "STORAGE_ENGINE": "INNODB",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "club_paddle",
        "USER": "club_paddle_user",
        "PASSWORD": "aca va el password que inventamos para la DB en MySQL",
    }
}

# idioma
LANGUAGE_CODE = "es-es"

# zona horaria
TIME_ZONE = "America/Argentina/Buenos_Aires"
```


# Instalar/actualizar dependencias de python y luego levantar el proyecto web

Abrir consola `cmd.exe` dentro de la ruta del repositorio `tp_hp`

`python.exe -m pip install --upgrade pip setuptools wheel`

`python.exe -m pip install -r requirements/base.txt -r requirements/dev.txt`

`cd club_paddle`

`python.exe manage.py migrate`

`python.exe manage.py createsuperuser --username admin --email ""`

Ejecutar el siguiente comando para levantar el proyecto web.
Esto va a quedar corriendo mientras funcione nuestro sitio web.
Para cortar su ejecución, hacer: `Ctrl + C`

`python.exe manage.py runserver`


# Ejemplos para acceder por navegador web

Esta es la URL de la administración propia de Django

http://127.0.0.1:8000/admin/

URLs de algunas pantallas del proyecto

http://127.0.0.1:8000/canchas/

http://127.0.0.1:8000/profesores/
