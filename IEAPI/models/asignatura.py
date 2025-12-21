from django.db import models

class Asignatura(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = "asignatura"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
