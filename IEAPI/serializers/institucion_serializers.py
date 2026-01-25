# IEAPI/serializers/institucion_serializers.py
from rest_framework import serializers
from IEAPI.models import InstitucionEducativa, NivelCatalogo

class NivelCatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelCatalogo
        fields = ['id', 'codigo', 'nombre']

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionEducativa
        fields = [
            'id', 'nombre', 'ruc', 'codigo_modular', 
            'direccion', 'ubigeo', 'es_activa'
        ]