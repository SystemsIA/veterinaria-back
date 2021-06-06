# Django
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from veterinaria_back.clases.models import Estado
from veterinaria_back.users.models import Notificacion

User = get_user_model()


@receiver(post_save, sender=Estado)
def post_save_estado(sender, instance: Estado, **kwargs):
    mascota = instance.historial.mascota
    data = {"cliente": mascota.duenio, "motivo": instance.descripcion}
    Notificacion.objects.create(**data)
