# IEAPI/models/anuncio.py
from django.db import models
from .seccion import Seccion
from .periodoLectivo import PeriodoLectivo
from .asignacion_rol import PersonalPeriodo

class Anuncio(models.Model):
    """
    Comunicados oficiales. El contenido es obligatorio para evitar anuncios vacíos.
    """
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name="anuncios")
    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.PROTECT)
    autor = models.ForeignKey(PersonalPeriodo, on_delete=models.PROTECT)
    
    titulo = models.CharField(max_length=200)
    contenido = models.TextField(help_text="Cuerpo del mensaje o comunicado") 
    fijado = models.BooleanField(default=False)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "anuncio"
        ordering = ["-fijado", "-creado_en"]

    def __str__(self):
        return f"{self.titulo} - {self.seccion}"