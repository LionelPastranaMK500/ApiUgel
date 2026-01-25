# IEAPI/serializers/matricula_serializers.py
from rest_framework import serializers
from IEAPI.models import Matricula

class MatriculaSerializer(serializers.ModelSerializer):
    """
    Serializer Puro: Estructura de Matrícula.
    """
    class Meta:
        model = Matricula
        fields = [
            'id', 'alumno', 'seccion', 
            'estado', 'fecha_inscripcion'
        ]