# IEAPI/serializers/configuracion_serializer.py

from rest_framework import serializers
from IEAPI.models import InstitucionEducativa

class InstitucionIdentidadSerializer(serializers.ModelSerializer):
    """Fase 2: Validador de entrada para la identidad de la IE"""
    class Meta:
        model = InstitucionEducativa
        fields = [
            'nombre', 'ruc', 'codigo_modular', 'codigo_local', 
            'direccion', 'ubigeo', 'telefono', 'email', 'web', 'logo'
        ]

class IEResponseSerializer(serializers.ModelSerializer):
    """Serializer para la salida de datos (Lectura)"""
    class Meta:
        model = InstitucionEducativa
        fields = '__all__'