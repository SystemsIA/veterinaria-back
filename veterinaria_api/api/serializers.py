# Django
from django.contrib.auth import authenticate, get_user_model, password_validation

# Rest
from rest_framework import serializers

# Model
from veterinaria_api.clases.models import (
    Cita,
    Especie,
    Estado,
    Historial,
    ImagenProducto,
    MarcaProducto,
    Mascota,
    Producto,
)
from veterinaria_api.users.models import Notificacion

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get("email"), password=data.get("password"))
        # Validación de contraseña
        if not user:
            raise serializers.ValidationError("Datos de acceso incorrectos.")
        # Validando usuario activo:
        if not user.activo:
            raise serializers.ValidationError(
                "El usuario no está activo. Comuniquese con el administrador."
            )
        # Validación tipo de usuario
        if not (user.tipo_usuario == User.CLIENTE or user.tipo_usuario == User.MEDICO):
            raise serializers.ValidationError("El usuario no es un cliente ni médico")
        data["user"] = user
        return data


class UserChaguePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        user = data.get("user")
        password1 = data.get("password1")
        password2 = data.get("password1")
        # Validación tipo de usuario
        if not (user.tipo_usuario == User.CLIENTE or user.tipo_usuario == User.MEDICO):
            raise serializers.ValidationError("El usuario no es un cliente ni médico")
        # Validando usuario activo:
        if not user.activo:
            raise serializers.ValidationError(
                "El usuario no está activo. Comuniquese con el administrador."
            )
        # Validando igualdad de password
        if password1 != password2:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        # Validado calidad de password
        password_validation.validate_password(password1)
        return data

    def create(self, data):
        user = data.get("user")
        password1 = data.get("password1")
        user.set_password(password1)
        user.save()
        return data


class UserModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nombre",
            "tipo_usuario",
            "dni",
            "direccion",
            "telefono",
            "activo",
        ]


# Mascotas
class EspecieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ["id", "tipo", "imagen"]


class MascotasModelSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.filter(tipo_usuario=User.CLIENTE),
        error_messages={"does_not_exist": "Este usuario no es cliente."},
    )
    especie_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Especie.objects.all()
    )
    especie = EspecieModelSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Mascota
        fields = [
            "id",
            "nombre",
            "especie",
            "edad",
            "raza",
            "color",
            "alergias",
            "sexo",
            "esterilizado",
            "entero",
            "gestacion",
            "lactancia",
            "dni",
            "user_id",
            "especie_id",
        ]

    def create(self, data):
        duenio = data.pop("user_id")
        especie = data.pop("especie_id")
        return Mascota.objects.create(**data, especie=especie, duenio=duenio)


# Clientes
class ClienteModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mascotas = MascotasModelSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nombre",
            "tipo_usuario",
            "dni",
            "direccion",
            "telefono",
            "password",
            "mascotas",
        ]
        read_only_fields = ["id", "tipo_usuario"]

    def create(self, data):
        username = str(data.get("nombre").replace(" ", "-"))
        return User.objects.create_user(
            **data, username=username, tipo_usuario=User.CLIENTE
        )


class NotificacionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ["motivo", "visto", "created"]


class CitaModelSerializer(serializers.ModelSerializer):
    cliente = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cita
        fields = ["id", "fecha_cita", "motivo", "cancelada", "atendida", "cliente"]
        read_only_fields = ["id", "atendida"]


#  Producto
class ProductoModelSerializer(serializers.ModelSerializer):
    class MarcaProductoModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = MarcaProducto
            fields = ["nombre", "imagen"]

    class ImagenProductoModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = ImagenProducto
            fields = ["imagen"]

    marca = MarcaProductoModelSerializer(read_only=True)
    imagenes = ImagenProductoModelSerializer(read_only=True, many=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "precio",
            "stock",
            "imagen_principal",
            "marca",
            "imagenes",
        ]


# Historial
class HistorialModelSerializer(serializers.ModelSerializer):
    medico = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mascota_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Mascota.objects.all()
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Historial
        fields = [
            "id",
            "descripcion",
            "talla",
            "peso",
            "tarea",
            "internado",
            "temperatura",
            "pulso",
            "diagnostico",
            "examen",
            "receta_medica",
            "medico",
            "mascota_id",
        ]

    def create(self, data):
        mascota = data.pop("mascota_id")
        return Historial.objects.create(**data, mascota=mascota)


class EstadoModelSerializer(serializers.ModelSerializer):
    historia_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Historial.objects.all()
    )

    class Meta:
        model = Estado
        fields = ["nombre", "descripcion", "created", "historia_id"]

    def create(self, data):
        historial = data.pop("historia_id")
        return Estado.objects.create(**data, historial=historial)
