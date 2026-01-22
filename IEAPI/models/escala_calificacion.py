# IEAPI/models/escala_calificacion.py
from django.db import models

class EscalaCalificacion(models.Model):
    """
    Define el método de calificación: Vigimal (0-20), Literal (AD-C), etc.
    Garantiza la Certeza Técnica ante cambios de normativa del MINEDU.
    """
    nombre = models.CharField(max_length=50) # 'Escala Vigimal', 'Escala Literal CNEB'
    es_literal = models.BooleanField(default=False)
    nota_minima = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    nota_maxima = models.DecimalField(max_digits=4, decimal_places=2, default=20)
    nota_aprobatoria = models.DecimalField(max_digits=4, decimal_places=2, default=10.5)

    class Meta:
        db_table = "escala_calificacion"

    def __str__(self):
        return self.nombre

class ValorEscala(models.Model):
    """
    Valores específicos para escalas literales (AD, A, B, C).
    """
    escala = models.ForeignKey(EscalaCalificacion, on_delete=models.CASCADE, related_name="valores")
    codigo = models.CharField(max_length=5) # 'AD', 'A', etc.
    leyenda = models.CharField(max_length=100) # 'Logro Destacado'
    valor_numerico = models.DecimalField(max_digits=4, decimal_places=2, help_text="Equivalencia para promedios")

    class Meta:
        db_table = "valor_escala"