# Django
from django.db import models

# Models
from model_utils.models import TimeStampedModel

# Utils
from veterinaria_api.utils import validators


# Producto
class MarcaProducto(TimeStampedModel):
    nombre = models.CharField(max_length=256)
    imagen = models.ImageField(upload_to="marca/img", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "Marcas"
        ordering = ["created", "modified"]


class Producto(TimeStampedModel):
    nombre = models.CharField(max_length=256)
    precio = models.FloatField(default=0.0)
    stock = models.SmallIntegerField(default=0)
    imagen_principal = models.ImageField(upload_to="producto/img", null=True)
    marca = models.ForeignKey(MarcaProducto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "03. Productos"
        ordering = ["created", "modified"]


class ImagenProducto(TimeStampedModel):
    imagen = models.ImageField(upload_to="producto/img", blank=True, null=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="imagenes"
    )

    def __str__(self):
        return str(self.producto.nombre)

    class Meta:
        ordering = ["created", "modified"]


# Mascota
class Especie(TimeStampedModel):
    FELINO = "FELINO"
    CANINO = "CANINO"
    AVE = "AVE"
    ACUATICO = "ACUATICO"
    ROEDOR = "ROEDOR"
    GANADO = "GANADO"
    TIPO_ESPECIE_CHOICES = [
        (FELINO, "FELINO"),
        (CANINO, "CANINO"),
        (AVE, "AVE"),
        (ACUATICO, "ACUATICO"),
        (ROEDOR, "ROEDOR"),
        (GANADO, "GANADO"),
    ]
    imagen = models.ImageField(upload_to="especie/img", blank=True, null=True)
    tipo = models.CharField(max_length=16, choices=TIPO_ESPECIE_CHOICES)

    def __str__(self):
        return str(self.tipo)

    class Meta:
        verbose_name = "especie"
        verbose_name_plural = "Especies"
        ordering = ["created", "modified"]


class Mascota(TimeStampedModel):
    MACHO = "MACHO"
    HEMBRA = "HEMBRA"
    SEXO_CHOICES = [(MACHO, "Macho"), (HEMBRA, "Hembra")]

    duenio = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="mascotas"
    )
    nombre = models.CharField(max_length=256)
    especie = models.ForeignKey(Especie, on_delete=models.SET_NULL, null=True)
    edad = models.CharField(max_length=256, blank=True)
    raza = models.CharField(max_length=256, blank=True)
    color = models.CharField(max_length=256, blank=True)
    alergias = models.TextField(max_length=2048, blank=True, null=True)
    sexo = models.CharField(choices=SEXO_CHOICES, max_length=8, null=True)
    esterilizado = models.BooleanField("esterilizado y/o castrado", default=False)
    entero = models.BooleanField(default=False)
    gestacion = models.BooleanField(default=False)
    lactancia = models.BooleanField(default=False)
    dni = models.CharField(
        "DNI o RUM",
        max_length=8,
        validators=[validators.dni_regex_validator],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Dueño: {self.duenio.nombre} | Mascota: {self.nombre}"

    class Meta:
        verbose_name = "mascota"
        verbose_name_plural = "01. Mascotas"
        ordering = ["-created", "-modified"]


# Historial
class Historial(TimeStampedModel):
    CONSULTA = "CONSULTA"
    CITA = "CITA"
    CIRUGIA = "CIRUGIA"
    VACUNA = "VACUNA"
    EXAMEN = "EXAMEN"
    TIPO_TAREA_CHOICE = [
        (CONSULTA, "CONSULTA"),
        (CITA, "CITA"),
        (CIRUGIA, "CIRUGIA"),
        (VACUNA, "VACUNA"),
        (EXAMEN, "EXAMEN"),
    ]
    medico = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="historiales"
    )
    descripcion = models.TextField(max_length=2048, blank=True, null=True)
    talla = models.CharField(max_length=256, blank=True)
    peso = models.FloatField(default=0.0, blank=True, null=True)
    tarea = models.CharField(max_length=16, choices=TIPO_TAREA_CHOICE)
    internado = models.BooleanField(default=False)
    temperatura = models.FloatField(default=0.0, blank=True, null=True)
    pulso = models.PositiveSmallIntegerField(default=0)
    diagnostico = models.TextField(max_length=2048, blank=True, null=True)
    examen = models.TextField(max_length=2048, blank=True, null=True)
    receta_medica = models.TextField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return f"Mascota: {self.mascota.nombre}"

    class Meta:
        verbose_name = "historial"
        verbose_name_plural = "04. Historiales"
        ordering = ["created", "modified"]


class Estado(TimeStampedModel):
    historial = models.ForeignKey(
        Historial, on_delete=models.CASCADE, related_name="estados"
    )
    nombre = models.CharField(max_length=256)
    descripcion = models.TextField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        ordering = ["created", "modified"]


# Cita
class Cita(TimeStampedModel):
    cliente = models.ForeignKey("users.User", on_delete=models.CASCADE)
    motivo = models.TextField(max_length=2048)
    fecha_cita = models.DateTimeField()
    cancelada = models.BooleanField(default=False)
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cliente.nombre)

    class Meta:
        verbose_name = "cita"
        verbose_name_plural = "02. Citas"
        ordering = ["fecha_cita", "created", "modified"]
