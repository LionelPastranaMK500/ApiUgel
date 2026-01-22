# IEAPI/models/componente_evaluacion.py
from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from .curso import Curso
from .tipoevaluacion import TipoEvaluacion

class ComponenteEvaluacion(models.Model):
    """
    Define un componente ponderado (porcentaje) dentro de un Curso y un periodo de tiempo.
    Resuelve la flexibilidad para Bimestres, Trimestres o Ciclos (Superior).
    """
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="componentes")
    
    # Reemplazamos el Choice rígido por una denominación dinámica
    # Ej: 'Bimestre 1', 'Unidad I', 'Ciclo 2026-I'
    denominacion_periodo = models.CharField(
        max_length=50, 
        help_text="Nombre del bloque evaluativo (Bimestre, Trimestre, etc.)"
    )
    
    tipo = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT, related_name="componentes")
    nombre = models.CharField(max_length=120) # Ej: "Examen Final", "Prácticas de Laboratorio"
    
    # El peso debe ser exacto para cálculos de promedios
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso porcentual (0.00 - 100.00)")
    
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, default="")

    class Meta:
        db_table = "componente_evaluacion"
        # La integridad se basa en no repetir un componente con el mismo nombre en el mismo periodo
        unique_together = (("curso", "denominacion_periodo", "nombre"),)
        indexes = [
            models.Index(fields=["curso", "denominacion_periodo"], name="idx_comp_curso_periodo"),
        ]
        ordering = ["curso", "denominacion_periodo", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.peso}%) · {self.curso} · {self.denominacion_periodo}"

    # --- Capa de Validación Fasética (Integridad de Datos) ---
    def clean(self):
        """
        Garantiza que la suma de pesos por curso y periodo no exceda el 100%.
        Mantra: 'Avanzamos para no volver atrás'. No permitimos datos inconsistentes.
        """
        if self.peso <= 0 or self.peso > Decimal("100.00"):
            raise ValidationError("El peso debe estar en el rango (0, 100].")

        # Cálculo de integridad para asegurar la Certeza Técnica
        qs = ComponenteEvaluacion.objects.filter(
            curso=self.curso, 
            denominacion_periodo=self.denominacion_periodo, 
            activo=True
        ).exclude(pk=self.pk)
        
        suma = qs.aggregate(total=models.Sum("peso"))["total"] or Decimal("0")
        
        if suma + self.peso > Decimal("100.00"):
            raise ValidationError(
                f"Error de Integridad: La suma de pesos en {self.denominacion_periodo} "
                f"excede el 100%. Acumulado actual: {suma}%"
            )

    @property
    def restante_en_periodo(self) -> Decimal:
        """Helper para que el profesor sepa cuánto peso le queda por asignar."""
        qs = ComponenteEvaluacion.objects.filter(
            curso=self.curso, 
            denominacion_periodo=self.denominacion_periodo, 
            activo=True
        ).exclude(pk=self.pk)
        suma = qs.aggregate(total=models.Sum("peso"))["total"] or Decimal("0")
        return Decimal("100.00") - suma