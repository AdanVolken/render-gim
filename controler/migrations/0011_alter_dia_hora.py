# Generated by Django 4.2.3 on 2023-11-15 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controler', '0010_cliente_rutina_alter_dia_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dia',
            name='hora',
            field=models.TimeField(default=datetime.time(7, 54, 56, 933708)),
        ),
    ]