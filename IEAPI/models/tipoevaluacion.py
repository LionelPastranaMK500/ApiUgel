from django.db import models

class TipoEvaluacion(models.Model):
    """
    Catálogo de tipos para clasificar componentes o evaluaciones.
    Ejemplos de códigos:
    autoevaluacion, videotest, tarea, entregable, examen_final, actitudes, participacion
    """
    codigo = models.SlugField(max_length=40, unique=True)
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = "tipo_evaluacion"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
