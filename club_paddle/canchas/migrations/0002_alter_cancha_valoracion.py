# Generated by Django 4.2.2 on 2023-10-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canchas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancha',
            name='valoracion',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
