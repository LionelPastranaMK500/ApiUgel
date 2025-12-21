from django.db import models
from django.conf import settings
from .curso import Curso

class Matricula(models.Model):
    ROLES = (("estudiante","Estudiante"),("docente","Docente"))

    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="matriculas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="matriculas")
    rol = models.CharField(max_length=10, choices=ROLES, default="estudiante")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matricula"
        unique_together = (("curso","usuario"),)
        indexes = [models.Index(fields=["curso","rol"], name="idx_matr_curso_rol")]
