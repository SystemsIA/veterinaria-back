# Django
from django.contrib.auth import authenticate, get_user_model, password_validation

# Rest
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from veterinaria_back.clases.models import (
    ImagenProducto,
    MarcaProducto,
    Mascota,
    Producto,
)

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
            raise serializers.ValidationError("El usuario no está activo. Comuniquese con el administrador.")
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
            raise serializers.ValidationError("El usuario no está activo. Comuniquese con el administrador.")
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
    class Meta:
        model = User
        fields = ["email", "nombre", "tipo_usuario", "dni", "direccion", "telefono", "activo"]


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
        fields = ["nombre", "precio", "stock", "imagen_principal", "marca", "imagenes"]


# Medico
class CrearClienteSerializer(serializers.Serializer):
    nombre = serializers.CharField(min_length=5)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=7)
    dni = serializers.CharField(min_length=8)
    direccion = serializers.CharField(required=False)
    telefono = serializers.CharField(min_length=9, max_length=12)

    def create(self, data):
        nombre = data.get("nombre")
        data = {
            "nombre": nombre,
            "email": data.get("email"),
            "username": nombre.replace(" ", "-"),
            "password": data.get("password"),
            "dni": data.get("dni"),
            "direccion": data.get("direccion", ""),
            "telefono": data.get("telefono"),
            "tipo_usuario": User.CLIENTE,
        }
        user = User.objects.create_user(**data, activo=True)
        return user


class MascotaSerializer(serializers.ModelSerializer):
    duenio = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = Mascota
        fields = ["duenio", "nombre", "edad", "descripcion", "especie", "raza"]
