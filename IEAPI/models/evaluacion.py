from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from .esquemaevaluacion import ComponenteEvaluacion

class Evaluacion(models.Model):
    componente = models.ForeignKey(ComponenteEvaluacion, on_delete=models.PROTECT, related_name="evaluaciones")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default="")
    fecha = models.DateField()                          # publicación/inicio
    fecha_cierre = models.DateField()                   # deadline decidido por el docente
    puntaje_max = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("20.00"))

    # 🔹 “Nota por atraso” editable (01 por defecto). No hay automatismos.
    nota_atraso = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("1.00"))

    activo = models.BooleanField(default=True)          # el docente puede cerrar/abrir si lo desea
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "evaluacion"
        indexes = [
            models.Index(fields=["componente"], name="idx_eval_componente"),
            models.Index(fields=["fecha_cierre"], name="idx_eval_cierre"),
        ]
        ordering = ["-fecha_cierre", "titulo"]

    def __str__(self):
        return f"{self.titulo} · {self.componente}"

    def clean(self):
        # Validaciones de rango
        if self.fecha_cierre < self.fecha:
            raise ValidationError("La fecha de cierre no puede ser anterior a la fecha de inicio.")

        # Fin del periodo del curso (curso → seccion → periodo)
        periodo_fin = self.componente.curso.seccion.periodo.fecha_fin
        if self.fecha_cierre > periodo_fin:
            raise ValidationError(f"La fecha de cierre no puede superar el fin del periodo ({periodo_fin}).")

        if self.nota_atraso < 0 or self.nota_atraso > self.puntaje_max:
            raise ValidationError("La nota por atraso debe estar entre 0 y el puntaje máximo.")

    # 🔹 Helper opcional: aplicar “nota por atraso” a quienes no tienen nota.
    #    Lo invoca manualmente el docente (por un botón/endpoint), NO se corre solo.
    def aplicar_nota_atraso(self, estudiantes_qs):
        """
        Crea Calificacion con 'nota_atraso' para quienes aún no tienen calificación.
        Retorna la cantidad creada. El docente decide CUÁNDO llamar esto.
        """
        from .calificacion import Calificacion
        existentes = set(
            Calificacion.objects.filter(evaluacion=self).values_list("estudiante_id", flat=True)
        )
        nuevos = [
            Calificacion(evaluacion=self, estudiante=est, nota=self.nota_atraso)
            for est in estudiantes_qs if est.id not in existentes
        ]
        if nuevos:
            Calificacion.objects.bulk_create(nuevos)
        return len(nuevos)
