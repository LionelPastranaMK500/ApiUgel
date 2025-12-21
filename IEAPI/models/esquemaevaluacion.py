from django.db import models
from decimal import Decimal
from .curso import Curso
from .tipoevaluacion import TipoEvaluacion

class ComponenteEvaluacion(models.Model):
    """
    Define un componente ponderado (porcentaje) dentro de un Curso y Bimestre.
    La suma de pesos por (curso, bimestre) debe ser 100.00.
    """
    BIMESTRES = [(i, f"Bimestre {i}") for i in range(1, 5)]  # 1..4

    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="componentes")
    bimestre = models.PositiveSmallIntegerField(choices=BIMESTRES)
    tipo = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT, related_name="componentes")
    nombre = models.CharField(max_length=120)                          # Ej: "Actitudes", "Participación"
    peso = models.DecimalField(max_digits=6, decimal_places=2)         # porcentaje (0–100)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, default="")

    class Meta:
        db_table = "componente_evaluacion"
        unique_together = (("curso", "bimestre", "nombre"),)
        indexes = [
            models.Index(fields=["curso", "bimestre"], name="idx_comp_curso_bim"),
        ]
        ordering = ["curso", "bimestre", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.peso}%) · {self.curso} · B{self.bimestre}"

    # --- Validaciones  (capa de modelo)
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.peso <= 0 or self.peso > Decimal("100.00"):
            raise ValidationError("El peso debe estar en (0, 100].")

        # Suma de pesos del resto de componentes + este
        qs = ComponenteEvaluacion.objects.filter(
            curso=self.curso, bimestre=self.bimestre, activo=True
        ).exclude(pk=self.pk)
        suma = qs.aggregate(total=models.Sum("peso"))["total"] or Decimal("0")
        if suma + self.peso > Decimal("100.00"):
            raise ValidationError(
                f"La suma de pesos en B{self.bimestre} excede 100%. Actual: {suma} + {self.peso}"
            )

    @property
    def restante_en_bimestre(self) -> Decimal:
        qs = ComponenteEvaluacion.objects.filter(
            curso=self.curso, bimestre=self.bimestre, activo=True
        ).exclude(pk=self.pk)
        suma = qs.aggregate(total=models.Sum("peso"))["total"] or Decimal("0")
        return Decimal("100.00") - suma
