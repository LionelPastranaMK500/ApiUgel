# IEAPI/serializers/estructura_serializers.py
from rest_framework import serializers
from IEAPI.models import Grado, Seccion

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = ['id', 'nombre', 'orden', 'nivel_tipo']

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = ['id', 'periodo', 'grado', 'letra', 'turno', 'modalidad', 'vacantes']