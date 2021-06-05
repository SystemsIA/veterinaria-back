# Django
from django.contrib.auth import get_user_model

# Rest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

# Serializers
from veterinaria_back.api.serializers import (
    CrearClienteSerializer,
    ProductoModelSerializer,
    UserChaguePasswordSerializer,
    UserModelSerializer,
)

# Model
from veterinaria_back.clases.models import Producto

User = get_user_model()


class DetailUser(RetrieveAPIView):
    serializer_class = UserModelSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.none()


class UserChangePassword(APIView):
    def post(self, request):
        serializer = UserChaguePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Contraseña cambiada correctamente"}, status=status.HTTP_200_OK)


# Producto
class ProductoModelViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductoModelSerializer
    permission_classes = [AllowAny]
    queryset = Producto.objects.all()


# Medico
class MedicoModelViewSet(ReadOnlyModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(tipo_usuario=User.MEDICO)

    @action(detail=False, methods=["post"])
    def crear_cliente(self, request):
        serializers = CrearClienteSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)


# class Medico
