# IEAPI/models/seccion.py
from django.db import models
from .grado import Grado
from .periodoLectivo import PeriodoLectivo

class Seccion(models.Model):
    class Turno(models.TextChoices):
        MANANA = "mañana", "Mañana"
        TARDE  = "tarde",  "Tarde"
        NOCHE  = "noche",  "Noche"

    class Modalidad(models.TextChoices):
        PRESENCIAL = "presencial", "Presencial"
        VIRTUAL    = "virtual", "Virtual"
        HIBRIDO    = "hibrido", "Híbrido"

    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.PROTECT, related_name="secciones")
    grado = models.ForeignKey(Grado, on_delete=models.PROTECT)
    letra = models.CharField(max_length=20, default="Única") # Soporta 'A', 'B', 'Especial', 'Única'
    turno = models.CharField(max_length=10, choices=Turno.choices, default=Turno.MANANA)
    modalidad = models.CharField(max_length=15, choices=Modalidad.choices, default=Modalidad.PRESENCIAL)
    vacantes = models.PositiveSmallIntegerField(default=30)

    class Meta:
        db_table = "seccion"
        unique_together = ('periodo', 'grado', 'letra', 'turno', 'modalidad')

    def __str__(self):
        return f"{self.grado.nombre} '{self.letra}' - {self.modalidad} ({self.periodo.anio})"