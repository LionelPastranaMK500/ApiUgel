# IEAPI/models/rol.py
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True) # 'Director', 'Profesor', etc.
    descripcion = models.TextField(blank=True)
    es_predeterminado = models.BooleanField(default=False) # Para proteger roles base

    class Meta:
        db_table = "rol"

    def __str__(self):
        return self.nombre