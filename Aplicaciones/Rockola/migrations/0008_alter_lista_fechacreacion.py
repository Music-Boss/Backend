# Generated by Django 4.0 on 2021-12-19 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rockola', '0007_amigo_delete_curso_delete_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista',
            name='fechaCreacion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
