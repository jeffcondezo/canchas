from rest_framework import serializers
from .models import Deporte


class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = ('id', 'descripcion', 'imagen')

