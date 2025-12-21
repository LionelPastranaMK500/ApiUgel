from django.db import models
from .institucionEducativa import InstitucionEducativa

class Niveleducativo(models.Model):
    institucion = models.OneToOneField(
        InstitucionEducativa,
        on_delete=models.PROTECT,     # evita borrar la institución si tiene niveles
        related_name="nivel"        # acceso: institucion.nivel
    )
    nvl_inicial    = models.BooleanField(default=False)
    nvl_primaria   = models.BooleanField(default=False)
    nvl_secundaria = models.BooleanField(default=False)
    nvl_superior   = models.BooleanField(default=False)
    descripcion    = models.TextField(blank=False, default="")

    class Meta:
        db_table = "nivel_educativo"

    def __str__(self):
        return f"Niveles de {self.institucion.nombre}"

    @property
    def niveles_activos(self) -> list[str]:
        activos = []
        if self.nvl_inicial:    activos.append("inicial")
        if self.nvl_primaria:   activos.append("primaria")
        if self.nvl_secundaria: activos.append("secundaria")
        if self.nvl_superior:   activos.append("superior")
        return activos
