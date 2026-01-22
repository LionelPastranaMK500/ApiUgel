# IEAPI/models/periodoLectivo.py
from django.db import models
from .institucionEducativa import InstitucionEducativa

class PeriodoLectivo(models.Model):
    """
    Define el año escolar cronológico. 
    Ejemplo: Año 2026.
    """
    institucion = models.ForeignKey(
        InstitucionEducativa, 
        on_delete=models.CASCADE, 
        related_name="periodos"
    )
    anio = models.PositiveSmallIntegerField() # Ej: 2026
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    es_periodo_actual = models.BooleanField(default=False)

    class Meta:
        db_table = "periodo_lectivo"
        unique_together = ('institucion', 'anio') # Una IE no puede tener dos "2026"
        ordering = ['-anio']

    def __str__(self):
        return f"{self.anio} - {self.institucion.nombre}"