# IEAPI/serializers/evaluacion_serializers.py
from rest_framework import serializers
from IEAPI.models import Evaluacion, TipoEvaluacion

class TipoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvaluacion
        fields = ['id', 'codigo', 'nombre']

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = [
            'id', 'curso', 'tipo', 'titulo', 
            'fecha_programada', 'descripcion', 'escala'
        ]