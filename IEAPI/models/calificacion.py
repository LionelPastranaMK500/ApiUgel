from django.db import models
from django.conf import settings
from decimal import Decimal
from .evaluacion import Evaluacion

class Calificacion(models.Model):
    """
    Nota de un estudiante en una evaluación específica.
    """
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.PROTECT, related_name="calificaciones")
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="calificaciones")
    nota = models.DecimalField(max_digits=6, decimal_places=2)   # 0..puntaje_max
    observado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "calificacion"
        unique_together = (("evaluacion", "estudiante"),)
        indexes = [
            models.Index(fields=["estudiante"], name="idx_calif_estudiante"),
            models.Index(fields=["evaluacion"], name="idx_calif_eval"),
        ]

    def __str__(self):
        return f"{self.estudiante} → {self.evaluacion} = {self.nota}"

    # --- Helpers de cálculo
    @property
    def aporte_porcentual(self) -> Decimal:
        """
        Aporte de esta calificación al % del bimestre del curso.
        Fórmula: (nota/puntaje_max) * peso_del_componente
        """
        comp = self.evaluacion.componente
        if self.evaluacion.puntaje_max == 0:
            return Decimal("0.00")
        ratio = Decimal(self.nota) / Decimal(self.evaluacion.puntaje_max)
        return (ratio * Decimal(comp.peso)).quantize(Decimal("0.01"))
