# IEAPI/models/calificacion.py
from django.db import models
from decimal import Decimal
from .evaluacion import Evaluacion
from .matricula import Matricula
from .escala_calificacion import ValorEscala 

class Calificacion(models.Model):
    """
    Nota final encapsulada por alumno y evaluación.
    Soporta notas numéricas (Superior) y literales (Básica).
    """
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.PROTECT, related_name="notas")
    # Vinculamos a la Matricula para asegurar que el alumno pertenece a la sección
    matricula = models.ForeignKey(Matricula, on_delete=models.PROTECT, related_name="calificaciones")
    
    # Nota Numérica (Fallback y para Superior)
    valor_numerico = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Nota Literal (Para Inicial/Primaria/Secundaria)
    valor_literal = models.ForeignKey(ValorEscala, on_delete=models.PROTECT, null=True, blank=True)
    
    observado = models.BooleanField(default=False)
    comentario_docente = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "calificacion"
        unique_together = (("evaluacion", "matricula"),)

    def __str__(self):
        nota = self.valor_literal.codigo if self.valor_literal else self.valor_numerico
        return f"{self.matricula.alumno.user.last_name} -> {nota}"

    @property
    def nota_final_display(self):
        """Helper para que el Frontend no sufra eligiendo qué mostrar."""
        return self.valor_literal.codigo if self.valor_literal else self.valor_numerico