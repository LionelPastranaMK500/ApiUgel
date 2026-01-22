# IEAPI/models/institucionEducativa.py
from django.db import models

class InstitucionEducativa(models.Model):
    # Identidad
    nombre = models.CharField(max_length=200, unique=True)
    ruc = models.CharField(max_length=11, unique=True, blank=True, null=True)
    codigo_modular = models.CharField(
        max_length=20, 
        unique=True, 
        help_text="Código identificador ante el MINEDU"
    )
    codigo_local = models.CharField(max_length=20, blank=True, null=True)
    
    # Contacto
    direccion = models.CharField(max_length=250)
    ubigeo = models.CharField(max_length=6, blank=True, null=True, help_text="Código de ubicación geográfica")
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)

    # Estado Operativo
    es_activa = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="ie/logos/", blank=True, null=True)

    class Meta:
        db_table = "institucion_educativa"
        verbose_name = "Institución Educativa"

    def __str__(self):
        return f"{self.nombre} ({self.codigo_modular})"