# IEAPI/serializers/niveles_serializer.py
from rest_framework import serializers
from IEAPI.models import InstitucionNivel

class AsignarNivelesSerializer(serializers.Serializer):
    """Fase 2: Valida la entrada para activar/desactivar niveles en la IE."""
    institucion_id = serializers.IntegerField()
    niveles = serializers.ListField(
        child=serializers.CharField(max_length=20),
        min_length=0  
    )

class InstitucionNivelReadSerializer(serializers.ModelSerializer):
    nombre_nivel = serializers.ReadOnlyField(source='nivel_tipo.nombre')
    codigo_nivel = serializers.ReadOnlyField(source='nivel_tipo.codigo')

    class Meta:
        model = InstitucionNivel
        # Cambiado es_activa -> es_activo
        fields = ['id', 'codigo_nivel', 'nombre_nivel', 'es_activo', 'fecha_activacion']