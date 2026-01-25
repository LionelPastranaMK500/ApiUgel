# IEAPI/serializers/malla_serializers.py
from rest_framework import serializers
from IEAPI.models import MallaCurricular, DetalleMalla

class DetalleMallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleMalla
        fields = ['id', 'grado', 'asignatura', 'horas_semanales']

class MallaCurricularSerializer(serializers.ModelSerializer):
    class Meta:
        model = MallaCurricular
        fields = ['id', 'nombre', 'nivel', 'anio_aprobacion', 'es_vigente']