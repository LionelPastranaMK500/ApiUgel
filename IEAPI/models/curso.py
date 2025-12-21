from django.db import models
from django.conf import settings
from .seccion import Seccion
from .asignatura import Asignatura

class Curso(models.Model):
    """
    Un curso (materia) que se dicta en una Sección durante un PeriodoLectivo.
    """
    seccion = models.ForeignKey(Seccion, on_delete=models.PROTECT, related_name="cursos")
    asignatura = models.ForeignKey(Asignatura, on_delete=models.PROTECT, related_name="cursos")
    docente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="cursos_dictados")
    estado = models.CharField(max_length=12, default="activo")  # activo/archivado
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "curso"
        unique_together = (("seccion", "asignatura"),)
        indexes = [models.Index(fields=["seccion"], name="idx_curso_seccion")]

    def __str__(self):
        return f"{self.asignatura} · {self.seccion}"
