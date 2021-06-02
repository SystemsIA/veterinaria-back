# Django
from django.db import models

# Models Utils
from model_utils.models import TimeStampedModel
from veterinaria_back.utils import validators
from ckeditor.fields import RichTextField


# Producto
class MarcaProducto(TimeStampedModel):
    nombre = models.CharField(max_length=256)
    imagen = models.ImageField("imagen", upload_to="marca/img", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "Marcas"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class Producto(TimeStampedModel):
    nombre = models.CharField(max_length=256)
    precio = models.FloatField(default=0.0)
    stock = models.SmallIntegerField(default=0)
    imagen_principal = models.ImageField("imagen", upload_to="producto/img", null=True)
    marca = models.ForeignKey(MarcaProducto, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "03. Productos"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class ImagenProducto(TimeStampedModel):
    imagen = models.ImageField("imagen", upload_to="producto/img", blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")

    def __str__(self):
        return str(self.producto.nombre)

    class Meta:
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


# Mascota
class Mascota(TimeStampedModel):
    MACHO = "MACHO"
    HEMBRA = "HEMBRA"
    SEXO_CHOICES = [(MACHO, "MACHO"), (HEMBRA, "HEMBRA")]

    duenio = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="mascotas")
    nombre = models.CharField(max_length=256)
    edad = models.CharField(max_length=256, blank=True)
    descripcion = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    especie = models.CharField(max_length=256, blank=True)
    raza = models.CharField(max_length=256, blank=True)
    alergias = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    color = models.CharField(max_length=256, blank=True)
    procedencia = models.CharField(max_length=256, blank=True)
    sexo = models.CharField(choices=SEXO_CHOICES, max_length=8, blank=True, null=True)
    estado_reproductivo = models.CharField(max_length=256, blank=True)
    dni = models.CharField(max_length=8, validators=[validators.dni_regex_validator], blank=True)

    def __str__(self):
        return f"Dueño: {self.duenio.nombre} | Mascota: {self.nombre}"

    class Meta:
        verbose_name = "mascota"
        verbose_name_plural = "01. Mascotas"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class Vacuna(TimeStampedModel):
    nombre = models.CharField(max_length=256)
    enfermedad = models.CharField(max_length=256)
    alergias = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    raza = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "vacuna"
        verbose_name_plural = "Vacunas"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class DetalleVacuna(TimeStampedModel):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mascota.nombre)

    class Meta:
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


# Historial
class Historial(TimeStampedModel):
    CIRUGIA = "CIRUGIA"
    VACUNA = "VACUNA"
    CONSULTA = "CONSULTA"
    CITA = "CITA"
    TIPO_TAREA_CHOICE = [
        (CONSULTA, "CONSULTA"),
        (CITA, "CITA"),
        (CIRUGIA, "CIRUGIA"),
        (VACUNA, "VACUNA"),
    ]
    medico = models.ManyToManyField("users.User")
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="historiales")
    tarea = models.CharField(max_length=16, choices=TIPO_TAREA_CHOICE, blank=True)
    talla = models.CharField(max_length=256, blank=True)
    peso = models.FloatField(blank=True)
    pulso = models.PositiveSmallIntegerField(default=0)
    internado = models.BooleanField(default=False)
    temperatura = models.FloatField(blank=True)
    pulso = models.PositiveSmallIntegerField(default=0)
    descripcion = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    diagnostico = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    examen = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)
    receta_medica = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)

    def __str__(self):
        return f"Medico: {self.medico.nombre} | mascota: {self.mascota.nombre}"

    class Meta:
        verbose_name = "historial"
        verbose_name_plural = "04. Historiales"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class Estado(TimeStampedModel):
    historial = models.ForeignKey(Historial, on_delete=models.CASCADE, related_name="estados")
    nombre = models.CharField(max_length=256)
    descripcion = RichTextField(help_text="Puedes colocar videos, imágenes y texto", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


# Cita
class Cita(TimeStampedModel):
    cliente = models.ForeignKey("users.User", on_delete=models.CASCADE)
    cancelada = models.BooleanField(default=False)
    fecha_cita = models.DateTimeField()
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cliente.nombre)

    class Meta:
        verbose_name = "cita"
        verbose_name_plural = "02. Citas"
        get_latest_by = "created"
        ordering = ["-created", "-modified"]
