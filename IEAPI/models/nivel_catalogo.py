# IEAPI/models/nivel_catalogo.py
from django.db import models

class NivelCatalogo(models.Model):
    """
    Catálogo maestro de niveles (Inicial, Primaria, Secundaria, Superior, CETPRO, etc.)
    """
    codigo = models.SlugField(max_length=20, unique=True) # ej: 'inicial', 'superior-tecnico'
    nombre = models.CharField(max_length=50) # ej: 'Educación Inicial'
    
    class Meta:
        db_table = "nivel_catalogo"
        verbose_name = "Nivel del Sistema Educativo"

    def __str__(self):
        return self.nombre