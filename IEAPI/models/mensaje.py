# IEAPI/models/mensaje.py
from django.db import models
from .usuario import PerfilPersona

class Conversacion(models.Model):
    """
    Contenedor de chat. El nombre es opcional para chats 1-1 y obligatorio para grupos.
    """
    nombre = models.CharField(max_length=120, blank=True, null=True, help_text="Nombre del grupo si aplica")
    es_grupal = models.BooleanField(default=False)
    participantes = models.ManyToManyField(PerfilPersona, related_name="conversaciones")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversacion"

class Mensaje(models.Model):
    """
    Cuerpo del mensaje enviado.
    """
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    emisor = models.ForeignKey(PerfilPersona, on_delete=models.PROTECT, related_name="enviados")
    texto = models.TextField() 
    leido_por = models.ManyToManyField(PerfilPersona, related_name="leidos", blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensaje"
        ordering = ["creado_en"]