# Generated by Django 4.2.7 on 2023-11-30 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0002_ejercicio_remove_rutina_imagen_rutina_ejercicios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejercicio',
            name='imagen',
            field=models.ImageField(upload_to='rutina/image/'),
        ),
    ]