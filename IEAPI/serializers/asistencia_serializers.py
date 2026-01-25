# IEAPI/serializers/asistencia_serializers.py
from rest_framework import serializers
from IEAPI.models import AsistenciaAlumno, AsistenciaPersonal

class AsistenciaAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaAlumno
        fields = ['id', 'matricula', 'fecha', 'estado', 'observacion']

class AsistenciaPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaPersonal
        fields = ['id', 'personal', 'fecha', 'hora_entrada', 'estado']