# Django
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

# Models Utils
from model_utils.models import TimeStampedModel
from veterinaria_back.utils import validators


class User(AbstractUser, TimeStampedModel):
    MEDICO = "MEDICO"
    CLIENTE = "CLIENTE"

    TIPO_USUARIO_CHOICES = [(MEDICO, "MEDICO"), (CLIENTE, "CLIENTE")]

    email = models.EmailField("correo electronico", unique=True)
    nombre = models.CharField("nombre completo", max_length=256)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    # raw_password = models.CharField("Unencrypted password", max_length=255, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=16, choices=TIPO_USUARIO_CHOICES, null=True, blank=True)
    dni = models.CharField(max_length=8, validators=[validators.dni_regex_validator], blank=True)
    direccion = models.CharField(max_length=256, blank=True)
    telefono = models.CharField(max_length=12, validators=[validators.celular_regex_validator], blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.nombre} | {self.email}"

    def set_password(self, raw_password):
        """Overwrite this method because we need to save the raw password to send the welcome mail with the password """
        self.password = make_password(raw_password)
        self._password = raw_password
        self.raw_password = raw_password

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]