# Django
from django.contrib.auth import get_user_model, authenticate

# Rest
from rest_framework import serializers

User = get_user_model()

# Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get("email"), password=data.get("password"))
        # Validación de contraseña
        if not user:
            raise serializers.ValidationError("Datos de acceso incorrectos.")
        # Validación tipo de usuario
        if not (user.tipo_usuario == User.CLIENTE or user.tipo_usuario == User.MEDICO):
            raise serializers.ValidationError("El usuario no es un cliente ni médico")
        data["user"] = user
        return data
