# IEAPI/models/evaluacion.py
from django.db import models
from .curso import Curso
from .escala_calificacion import EscalaCalificacion

class TipoEvaluacion(models.Model):
    """
    Categoría de la nota. Ej: 'Examen Parcial', 'Tarea', 'Participación'.
    """
    nombre = models.CharField(max_length=50)
    peso_porcentual = models.PositiveSmallIntegerField(default=25) # Ej: 25% de la nota final

    class Meta:
        db_table = "tipo_evaluacion"

class Evaluacion(models.Model):
    """
    Una actividad evaluativa concreta creada por el profesor.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="evaluaciones")
    tipo = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)
    fecha_programada = models.DateField()
    descripcion = models.TextField(blank=True)
    
    # Cada evaluación puede tener su propia escala según el nivel
    escala = models.ForeignKey(EscalaCalificacion, on_delete=models.PROTECT)

    class Meta:
        db_table = "evaluacion"