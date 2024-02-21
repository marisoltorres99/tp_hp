# tp_hp

Repositorio Git para el proyecto Django.

# Instalar virtualenv + pip

Para instalarlo y luego crearlo ejecutamos:

`apt install python3-virtualenv`

`cd <carpeta_del_repositorio_git>`

`virtualenv -p /usr/bin/python3.10 --prompt "(virtualenv-PWC)" virtualenv`

Activar el virtualenv recién creado y luego actualizar pip:

`source virtualenv/bin/activate`

Descargar e instalar pip por medio del script get-pip.py:

`curl -sS https://bootstrap.pypa.io/get-pip.py | python3`

Luego actualizamos pip mas otras deps relacionadas:

`pip install --upgrade pip setuptools wheel`

# Instalar dependencias de Python para compilar lib de MySQL (MariaDB)

`apt install build-essential`

`apt install python3-dev`

`apt install default-libmysqlclient-dev`

# Instalar/actualizar requirements del proyecto Django

`pip install -r requirements/base.txt -r requirements/dev.txt`

# Crear el proyecto Django

`django-admin startproject <carpeta_del_proyecto_django>`

# Crear DB en MySQL, crear usuario para DB y asignar permisos

```
CREATE DATABASE nombre_db
    DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_spanish_ci;

CREATE USER 'usuario_db'@'localhost' IDENTIFIED BY 'completar password';

GRANT ALL PRIVILEGES ON nombre_db.* TO 'usuario_db'@'localhost';
```

# Modificar estructura de settings para convertirlo en un package

`cd <carpeta_del_proyecto_django>`

`mkdir <carpeta_del_proyecto_django>/settings/`

`mv -v <carpeta_del_proyecto_django>/settings.py <carpeta_del_proyecto_django>/settings/django_base.py`

# Crear nuestro archivo de configs personalizadas

`touch <carpeta_del_proyecto_django>/settings/__init__.py`

Agregar el siguiente contenido al archivo **<carpeta_del_proyecto_django>/settings/\_\_init\_\_.py**:

```
from .django_base import *

# datos acceso DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "STORAGE_ENGINE": "INNODB",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "nombre_db",
        "USER": "usuario_db",
        "PASSWORD": "completar password",
    }
}

# idioma
LANGUAGE_CODE = "es-es"

# zona horaria
TIME_ZONE = "America/Argentina/Buenos_Aires"
```

# Correr migrations

Ahora se creará todo en la DB MySQL

`python manage.py migrate`

# Crear usuario admin

`python manage.py createsuperuser --username admin`

# Levantar el server de desarrollo

`python manage.py runserver`

# Acceder a la administración

Podemos acceder a la administración con el usuario creado anteriormente
y allí crear mas usuarios, editar, etc...

    http://127.0.0.1:8000/admin/

# borrador
mariadb-tzinfo-to-sql /usr/share/zoneinfo | mariadb -u root mysql

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

ver cron
