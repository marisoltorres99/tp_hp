# Generated by Django 4.2.2 on 2024-02-23 00:57

import canchas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0003_cancha_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancha',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=canchas.models.get_img_upload_path),
        ),
    ]
