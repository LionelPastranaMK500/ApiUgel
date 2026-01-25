# IEAPI/serializers/interaccion_serializers.py
from rest_framework import serializers
from IEAPI.models import Anuncio, DebateTema, DebatePost, Conversacion, Mensaje

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['id', 'seccion', 'periodo', 'autor', 'titulo', 'contenido', 'fijado', 'creado_en']

class DebateTemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateTema
        fields = [
            'id', 'curso', 'titulo', 'descripcion', 
            'creador_personal', 'creador_alumno', 'cerrado', 'creado_en'
        ]

class DebatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebatePost
        fields = ['id', 'tema', 'parent', 'autor_personal', 'autor_alumno', 'contenido', 'creado_en']

class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ['id', 'nombre', 'es_grupal', 'participantes', 'creado_en']

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['id', 'conversacion', 'emisor', 'texto', 'leido_por', 'creado_en']