# IEAPI/models/asignatura.py
from django.db import models

class Asignatura(models.Model):
    """
    Catálogo maestro de materias. 
    Base inmutable para la construcción de mallas[cite: 115, 189].
    """
    nombre = models.CharField(max_length=120, unique=True)
    codigo_sigla = models.CharField(max_length=10, unique=True, blank=True, null=True)

    class Meta:
        db_table = "asignatura"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre