from django.db import models

class InstitucionEducativa(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo_modular = models.CharField(max_length=20, blank=True, null=True, unique=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = "institucion_educativa"

    def __str__(self):
        return self.nombre