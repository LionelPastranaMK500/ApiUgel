# IEAPI/serializers/calificacion_serializers.py
from rest_framework import serializers
from IEAPI.models import Calificacion, ValorEscala

class ValorEscalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValorEscala
        fields = ['id', 'codigo', 'leyenda', 'valor_numerico']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = [
            'id', 'evaluacion', 'matricula', 
            'valor_numerico', 'valor_literal', 
            'observado', 'comentario_docente'
        ]