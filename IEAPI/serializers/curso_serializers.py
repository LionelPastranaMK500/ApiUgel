# IEAPI/serializers/curso_serializers.py
from rest_framework import serializers
from IEAPI.models import Curso

class CursoSerializer(serializers.ModelSerializer):
    """
    Serializer Puro: Contenedor de datos para Cursos.
    """
    class Meta:
        model = Curso
        fields = [
            'id', 'periodo', 'seccion', 
            'detalle_malla', 'docente_responsable'
        ]