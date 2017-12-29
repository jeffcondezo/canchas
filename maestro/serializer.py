from rest_framework import serializers
from .models import Deporte, Sucursal, Distrito
from django.contrib.auth.models import User


class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = ('id', 'descripcion', 'imagen')


class SucursalSerializer(serializers.ModelSerializer):
    distrito = serializers.SlugRelatedField(
        slug_field='descripcion',
        read_only=True,
     )

    class Meta:
        model = Sucursal
        fields = ('id', 'descripcion', 'distrito', 'latitud', 'longitud')


class HorarioxSucursalSerial(serializers.Serializer):
    timeinicio = serializers.TimeField()
    horainicio = serializers.IntegerField()


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    celular = serializers.CharField(source='usuario.phonenumber')

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'celular')

