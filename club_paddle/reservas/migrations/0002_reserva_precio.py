# Generated by Django 4.2.2 on 2024-01-26 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='precio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
