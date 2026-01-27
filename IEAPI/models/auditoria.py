# IEAPI/models/auditoria.py
from django.db import models
from django.conf import settings

class LogAuditoria(models.Model):
    """
    Fase 1: Almacén de seguridad.
    Registra quién hizo qué para evitar el 'pendejismo'.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=100) # Ej: 'REGISTRO_MATRICULA'
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "log_auditoria"
        ordering = ["-fecha_evento"]

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha_evento}"