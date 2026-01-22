# IEAPI/models/asistencia.py
from django.db import models
from .matricula import Matricula
from .asignacion_rol import PersonalPeriodo

class AsistenciaAlumno(models.Model):
    """
    Registro diario por alumno. 
    Crucial para traslados: la asistencia queda amarrada a la matrícula de ese momento.
    """
    class Estado(models.TextChoices):
        PRESENTE    = "P", "Presente"
        FALTA       = "F", "Falta"
        TARDANZA    = "T", "Tardanza"
        JUSTIFICADA = "J", "Justificada"

    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name="asistencias")
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=Estado.choices)
    observacion = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "asistencia_alumno"
        unique_together = ('matricula', 'fecha') # No puede tener dos asistencias el mismo día

class AsistenciaPersonal(models.Model):
    """
    Registro para docentes y administrativos. 
    Usa el registro de personal encapsulado del año.
    """
    personal = models.ForeignKey(PersonalPeriodo, on_delete=models.CASCADE, related_name="asistencias")
    fecha = models.DateField()
    hora_entrada = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=1, choices=AsistenciaAlumno.Estado.choices)

    class Meta:
        db_table = "asistencia_personal"
        unique_together = ('personal', 'fecha')