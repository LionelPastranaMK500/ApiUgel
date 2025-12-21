from django.db import models

class PeriodoLectivo(models.Model):
    """
    Año escolar de la institución. Único por año.
    """
    anio = models.PositiveSmallIntegerField(unique=True)          # ej: 2025
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = "periodo_lectivo"
        ordering = ["-anio"]

    def __str__(self):
        return str(self.anio)