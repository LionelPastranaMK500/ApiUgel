from rest_framework import serializers
from IEAPI.models import InstitucionNivel

class InstitucionNivelReadSerializer(serializers.ModelSerializer):
    """Serializer para listar el estado de los niveles de la IE."""
    nombre_nivel = serializers.ReadOnlyField(source='nivel_tipo.nombre')
    codigo_nivel = serializers.ReadOnlyField(source='nivel_tipo.codigo')

    class Meta:
        model = InstitucionNivel
        fields = ['id', 'codigo_nivel', 'nombre_nivel', 'es_activo', 'fecha_activacion']