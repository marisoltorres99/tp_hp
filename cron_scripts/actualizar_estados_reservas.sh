#!/bin/bash

source "../virtualenv/bin/activate"

cd "../club_paddle/"

python manage.py actualizar_estado
