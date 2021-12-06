# Generated by Django 3.2.9 on 2021-12-06 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clases', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='duenio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mascotas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mascota',
            name='especie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clases.especie'),
        ),
        migrations.AddField(
            model_name='imagenproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='clases.producto'),
        ),
        migrations.AddField(
            model_name='historial',
            name='mascota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historiales', to='clases.mascota'),
        ),
        migrations.AddField(
            model_name='historial',
            name='medico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estado',
            name='historial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='clases.historial'),
        ),
        migrations.AddField(
            model_name='cita',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
