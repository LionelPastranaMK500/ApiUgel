# IEAPI/serializers/usuario_serializers.py
from rest_framework import serializers
from IEAPI.models import PerfilPersona, Rol, AsignacionRol, PersonalPeriodo

class PerfilPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilPersona
        fields = ['id', 'user', 'dni', 'fecha_nacimiento', 'genero']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'es_predeterminado']

class AsignacionRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionRol
        fields = ['id', 'persona', 'institucion', 'rol', 'esta_activo']

class PersonalPeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalPeriodo
        fields = [
            'id', 'persona', 'rol', 'periodo', 
            'area_departamento', 'fecha_inicio', 'fecha_fin', 
            'es_titular', 'observaciones_gestion'
        ]