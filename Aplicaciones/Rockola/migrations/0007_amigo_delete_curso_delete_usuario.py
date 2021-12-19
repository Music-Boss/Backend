# Generated by Django 4.0 on 2021-12-19 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Rockola', '0006_alter_cancion_artista'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amigo',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usuario', serialize=False, to='auth.user')),
                ('amigos', models.ManyToManyField(blank=True, related_name='amigos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
