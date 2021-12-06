# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Models Utils
from model_utils.models import TimeStampedModel

from veterinaria_api.utils import validators


class User(AbstractUser, TimeStampedModel):
    MEDICO = "MEDICO"
    CLIENTE = "CLIENTE"

    TIPO_USUARIO_CHOICES = [(MEDICO, "MEDICO"), (CLIENTE, "CLIENTE")]

    email = models.EmailField("correo electronico", unique=True)
    nombre = models.CharField("nombre completo", max_length=256)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    tipo_usuario = models.CharField(
        max_length=16, choices=TIPO_USUARIO_CHOICES, null=True, blank=True
    )
    dni = models.CharField(
        max_length=8, validators=[validators.dni_regex_validator], blank=True
    )
    direccion = models.CharField(max_length=256, blank=True)
    telefono = models.CharField(
        max_length=12, validators=[validators.celular_regex_validator], blank=True
    )
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.nombre} | {self.email} | {self.tipo_usuario}"

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["-created", "-modified"]


class Notificacion(TimeStampedModel):
    cliente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificaciones"
    )
    motivo = models.TextField(max_length=1024)
    visto = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cliente.nombre)

    class Meta:
        verbose_name = "notificaion"
        verbose_name_plural = "Notificaciones"
        ordering = ["created", "modified"]
