# IEAPI/models/niveleducativo.py (Refactorizado)
from django.db import models
from .institucionEducativa import InstitucionEducativa
from .nivel_catalogo import NivelCatalogo

class InstitucionNivel(models.Model):
    """
    Tabla intermedia que define qué niveles ofrece UNA institución específica.
    Permite que una IE tenga solo Inicial, o Inicial + Primaria + Superior.
    """
    institucion = models.ForeignKey(
        InstitucionEducativa, 
        on_delete=models.CASCADE, 
        related_name="niveles_configurados"
    )
    nivel_tipo = models.ForeignKey(
        NivelCatalogo, 
        on_delete=models.PROTECT
    )
    fecha_activacion = models.DateField(auto_now_add=True)
    es_activo = models.BooleanField(default=True)

    class Meta:
        db_table = "institucion_nivel"
        unique_together = ('institucion', 'nivel_tipo') # Evita duplicar el mismo nivel en la IE

    def __str__(self):
        return f"{self.institucion.nombre} - {self.nivel_tipo.nombre}"