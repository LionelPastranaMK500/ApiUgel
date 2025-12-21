from django.db import models
from .grado import Grado
from .periodoLectivo import PeriodoLectivo

class Seccion(models.Model):
    """
    Una sección (aula) concreta del colegio.
    """
    class Turno(models.TextChoices):
        MANANA = "mañana", "Mañana"
        TARDE  = "tarde",  "Tarde"
        NOCHE  = "noche",  "Noche"

    grado = models.ForeignKey(Grado, on_delete=models.PROTECT, related_name="secciones")
    letra = models.CharField(max_length=5)                         # ej: "A", "B"
    turno = models.CharField(max_length=10, choices=Turno.choices, default=Turno.MANANA)
    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.PROTECT, related_name="secciones")
    # tutor_id lo dejamos para cuando conectes usuarios:
    # tutor_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "seccion"
        unique_together = (("grado", "letra", "turno", "periodo"),)
        indexes = [
            models.Index(fields=["periodo"], name="idx_seccion_periodo"),
            models.Index(fields=["grado"], name="idx_seccion_grado"),
        ]
        ordering = ["-periodo", "grado__nivel", "grado__orden", "letra"]

    def __str__(self):
        return f"{self.grado} - {self.letra} ({self.get_turno_display()} · {self.periodo})"
