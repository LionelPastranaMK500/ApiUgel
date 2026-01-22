# IEAPI/models/asignatura.py
from django.db import models

class Asignatura(models.Model):
    """
    Catálogo de materias. 
    Corregido: Se quita unique=True del nombre para permitir colisiones entre niveles.
    """
    nombre = models.CharField(max_length=120) 
    codigo_sigla = models.CharField(max_length=20, unique=True, help_text="ID único interno (ej: MAT-PRI-2025)")

    class Meta:
        db_table = "asignatura"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_sigla})"