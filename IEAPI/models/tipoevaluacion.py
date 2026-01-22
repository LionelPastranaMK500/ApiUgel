# IEAPI/models/tipo_evaluacion.py
from django.db import models

class TipoEvaluacion(models.Model):
    """
    Catálogo de tipos: Tarea, Examen, Participación.
    """
    codigo = models.SlugField(max_length=40, unique=True)
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = "tipo_evaluacion"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre