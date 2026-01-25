# IEAPI/serializers/periodo_serializers.py
from rest_framework import serializers
from IEAPI.models import PeriodoLectivo

class PeriodoLectivoSerializer(serializers.ModelSerializer):
    """
    Serializer Puro: Definición temporal del periodo.
    """
    class Meta:
        model = PeriodoLectivo
        fields = ['id', 'anio', 'fecha_inicio', 'fecha_fin', 'es_periodo_actual']