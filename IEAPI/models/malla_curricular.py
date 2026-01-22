# IEAPI/models/malla_curricular.py
from django.db import models
from .nivel_catalogo import NivelCatalogo
from .asignatura import Asignatura
from .grado import Grado

class MallaCurricular(models.Model):
    """
    Define el plan de estudios vigente. 
    Permite evolucionar el currículo sin romper el pasado[cite: 130, 242].
    """
    nombre = models.CharField(max_length=100) # Ej: 'Plan 2025 - Superior'
    nivel = models.ForeignKey(NivelCatalogo, on_delete=models.PROTECT)
    anio_aprobacion = models.PositiveSmallIntegerField()
    es_vigente = models.BooleanField(default=True)

    class Meta:
        db_table = "malla_curricular"

    def __str__(self):
        return f"{self.nombre} ({self.nivel.nombre})"

class DetalleMalla(models.Model):
    """
    Especificación de materias por grado dentro de una malla.
    Resuelve la flexibilidad de años de estudio (1-5, 1-7, etc.)[cite: 115, 134].
    """
    malla = models.ForeignKey(MallaCurricular, on_delete=models.CASCADE, related_name="detalles")
    grado = models.ForeignKey(Grado, on_delete=models.PROTECT)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.PROTECT)
    horas_semanales = models.PositiveSmallIntegerField(default=4)

    class Meta:
        db_table = "detalle_malla"
        unique_together = ('malla', 'grado', 'asignatura')