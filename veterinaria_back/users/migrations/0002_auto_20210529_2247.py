# Generated by Django 3.1.11 on 2021-05-30 03:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified'], 'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios'},
        ),
        migrations.AlterField(
            model_name='user',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message="El celular puede comenzar con '+' o tener mín 9 y máx 12 dígitos.", regex='\\+?1?\\d{9,12}$')]),
        ),
    ]