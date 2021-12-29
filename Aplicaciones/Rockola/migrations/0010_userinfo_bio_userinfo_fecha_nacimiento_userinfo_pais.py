# Generated by Django 4.0 on 2021-12-29 17:17

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Rockola', '0009_rename_amigo_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='pais',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]