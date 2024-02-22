# tp_hp

Repositorio Git para el proyecto Django.

# Instalar virtualenv + pip

Para instalarlo y luego crearlo ejecutamos:

`cd <carpeta_del_repositorio_git>`

`apt install python3-virtualenv`

`virtualenv -p /usr/bin/python3.10 --prompt "(virtualenv-TP_HP)" virtualenv`

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

# Crear el proyecto Django (solo la primera vez)

`django-admin startproject <carpeta_del_proyecto_django>`

# Modificar estructura de settings para convertirlo en un package (solo la primera vez)

`cd <carpeta_del_proyecto_django>`

`mkdir <carpeta_del_proyecto_django>/settings/`

`mv -v <carpeta_del_proyecto_django>/settings.py <carpeta_del_proyecto_django>/settings/django_base.py`

# Crear DB en MySQL, crear usuario para DB y asignar permisos (solo si no existe)

```
CREATE DATABASE club_paddle DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_spanish_ci;

CREATE USER 'club_paddle_user'@'localhost' IDENTIFIED BY 'completar password';

GRANT ALL PRIVILEGES ON club_paddle.* TO 'club_paddle_user'@'localhost';
```

# Cargar time zone info en la DB

Para MariaDB ejecutar:

`mariadb-tzinfo-to-sql /usr/share/zoneinfo | sudo mariadb -u root mysql`

Para MySQL ejecutar:

`mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root mysql`

# Crear nuestro archivo de configs personalizadas copiando el archivo de ejemplo y luego editarlo

Crear una copia del archivo `tp_hp/club_paddle/club_paddle/settings/example_init.py`
Y renombrar la copia como `__init__.py`
Luego editar el contenido de la copia para ajustar nuestros passwords.

# Correr migrations

Ahora se creará todo en la DB MySQL

`cd tp_hp/club_paddle/`

`python manage.py migrate`

# Crear usuario admin

`python manage.py createsuperuser --username admin`

# Levantar el server de desarrollo

`python manage.py runserver`

# Acceder a la administración

Podemos acceder a la administración con el usuario creado anteriormente
y allí crear mas usuarios, editar, etc...

    http://127.0.0.1:8000/admin/

# Configurar croneo de script para actualizar estados de reservas

`crontab -e`

Y luego agregar la config:

```
0 * * * * /ruta_repositorio_git/cron_scripts/actualizar_estados_reservas.sh
```
