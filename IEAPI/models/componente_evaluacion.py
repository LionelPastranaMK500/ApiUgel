# IEAPI/models/componente_evaluacion.py
from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from .curso import Curso
from .evaluacion import TipoEvaluacion

class ComponenteEvaluacion(models.Model):
    """
    Define un componente ponderado dentro de un Curso y un periodo dinámico.
    Corregido: Uso de 'condition' en CheckConstraint para compatibilidad con Django 5.x/6.0.
    """
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="componentes")
    denominacion_periodo = models.CharField(
        max_length=50, 
        help_text="Ej: 'Bimestre 1', 'Ciclo 2026-I'"
    )
    tipo = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT, related_name="componentes")
    nombre = models.CharField(max_length=120) 
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso (0.01 - 100.00)")
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, default="")

    class Meta:
        db_table = "componente_evaluacion"
        unique_together = (("curso", "denominacion_periodo", "nombre"),)
        ordering = ["curso", "denominacion_periodo", "nombre"]
        indexes = [
            models.Index(fields=["curso", "denominacion_periodo"], name="idx_comp_curso_periodo"),
        ]
        # BLINDAJE SQL ACTUALIZADO: Se usa 'condition' en lugar de 'check'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(peso__gt=0) & models.Q(peso__lte=100),
                name="ck_peso_rango_valido"
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.peso}%) · {self.curso} · {self.denominacion_periodo}"

    def clean(self):
        if self.peso <= 0 or self.peso > Decimal("100.00"):
            raise ValidationError("El peso debe estar entre 0.01 y 100.00.")

        qs = ComponenteEvaluacion.objects.filter(
            curso=self.curso, 
            denominacion_periodo=self.denominacion_periodo, 
            activo=True
        ).exclude(pk=self.pk)
        
        suma = qs.aggregate(total=models.Sum("peso"))["total"] or Decimal("0")
        
        if suma + self.peso > Decimal("100.00"):
            raise ValidationError(
                f"Error de Integridad: La suma de pesos en {self.denominacion_periodo} "
                f"excede el 100%. Ya tienes {suma}% asignado."
            )