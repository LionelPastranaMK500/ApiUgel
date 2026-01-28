from rest_framework import serializers
from IEAPI.models import PeriodoLectivo

class PeriodoSimpleSerializer(serializers.ModelSerializer):
    """Para listados rápidos: solo lo esencial."""
    class Meta:
        model = PeriodoLectivo
        fields = ['id', 'anio', 'es_periodo_actual']

class PeriodoFullSerializer(serializers.ModelSerializer):
    """Para el detalle completo, creación y edición."""
    class Meta:
        model = PeriodoLectivo
        fields = ['id', 'anio', 'fecha_inicio', 'fecha_fin', 'es_periodo_actual']