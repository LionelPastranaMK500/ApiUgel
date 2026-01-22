from django.db import models
from .nivel_catalogo import NivelCatalogo

class Grado(models.Model):
    """
    Define los grados o ciclos pertenecientes a un nivel.
    Resuelve el caso de secundarias de 5 años o institutos de 7+ ciclos.
    """
    nivel_tipo = models.ForeignKey(
        NivelCatalogo, 
        on_delete=models.PROTECT, 
        related_name="grados"
    )
    nombre = models.CharField(max_length=50) # '1° Grado', '7° Ciclo', 'Aula Roja'
    orden = models.PositiveSmallIntegerField(
        help_text="Orden correlativo para certificados (1, 2, 3...)"
    )

    class Meta:
        db_table = "grado"
        unique_together = ('nivel_tipo', 'nombre')
        ordering = ['nivel_tipo', 'orden']

    def __str__(self):
        return f"{self.nombre} - {self.nivel_tipo.nombre}"