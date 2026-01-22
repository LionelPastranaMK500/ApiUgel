# IEAPI/models/curso.py
from django.db import models
from .seccion import Seccion
from .malla_curricular import DetalleMalla
from .asignacion_rol import PersonalPeriodo 

class Curso(models.Model):
    """
    Instancia real de una materia en un salón.
    Une la malla con el docente responsable del periodo[cite: 148, 194].
    """
    seccion = models.ForeignKey(Seccion, on_delete=models.PROTECT, related_name="cursos")
    detalle_malla = models.ForeignKey(DetalleMalla, on_delete=models.PROTECT)
    
    docente_responsable = models.ForeignKey(
        PersonalPeriodo, 
        on_delete=models.PROTECT, 
        limit_choices_to={'rol__nombre__icontains': 'Profesor'},
        related_name="cursos_dictados"
    )

    class Meta:
        db_table = "curso"
        unique_together = ('seccion', 'detalle_malla')

    def __str__(self):
        return f"{self.detalle_malla.asignatura.nombre} - {self.seccion}"