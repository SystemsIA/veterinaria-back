# Django
from django.contrib.auth import get_user_model

# Rest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

# Serializers
from veterinaria_back.api.serializers import (
    ProductoModelSerializer,
    UserChaguePasswordSerializer,
    UserModelSerializer,
    ClienteModelSerializer,
    MascotasModelSerializer,
    EspecieModelSerializer,
    NotificacionModelSerializer,
    HistorialModelSerializer,
    EstadoModelSerializer,
    CitaModelSerializer,
)

# Model
from veterinaria_back.clases.models import Cita, Especie, Estado, Historial, Mascota, Producto
from veterinaria_back.users.models import Notificacion

# pagination
from veterinaria_back.api.pagination import NotificacionPagination

User = get_user_model()


class DetailUserApiView(RetrieveAPIView):
    serializer_class = UserModelSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.none()

    def get_serializer_class(self):
        if self.request.user.tipo_usuario == User.CLIENTE:
            return ClienteModelSerializer
        return super().get_serializer_class()


class NotificacionUserApiView(ListAPIView):
    serializer_class = NotificacionModelSerializer
    pagination_class = NotificacionPagination

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return Notificacion.objects.filter(cliente=self.get_object())


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


# Mascota
class EspecieModelViewSet(ReadOnlyModelViewSet):
    serializer_class = EspecieModelSerializer
    permission_classes = [AllowAny]
    queryset = Especie.objects.all()


class MascotaModelViewSet(ReadOnlyModelViewSet):
    serializer_class = MascotasModelSerializer
    queryset = Mascota.objects.all()

    @action(detail=True, methods=["GET", "POST"])
    def historias(self, request, pk, *args, **kwargs):
        if request.method == "POST":
            data = request.data
            data["mascota_id"] = pk
            serializer = HistorialModelSerializer(data=data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Historial.objects.filter(mascota_id=pk)
        serializer = HistorialModelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Cliente
class ClienteModelViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    serializer_class = ClienteModelSerializer
    queryset = User.objects.filter(tipo_usuario=User.CLIENTE)

    @action(detail=True, methods=["POST"])
    def mascotas(self, request, pk, *args, **kwargs):
        data = request.data
        data["user_id"] = pk
        data["especie_id"] = request.data.get("especie")
        serializer = MascotasModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CitaModelViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CitaModelSerializer
    queryset = Cita.objects.all()


# Medico
class MedicoModelViewSet(ReadOnlyModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(tipo_usuario=User.MEDICO)


class HistoriasModelViewSet(ReadOnlyModelViewSet):
    serializer_class = HistorialModelSerializer
    queryset = Historial.objects.all()

    @action(detail=True, methods=["GET", "POST"])
    def estados(self, request, pk, *args, **kwargs):
        if request.method == "POST":
            data = request.data
            data["historia_id"] = pk
            serializer = EstadoModelSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        queryset = Estado.objects.filter(historial_id=pk)
        serializer = EstadoModelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
