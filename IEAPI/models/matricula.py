# IEAPI/models/matricula.py
from django.db import models
from .usuario import PerfilPersona
from .seccion import Seccion

class Matricula(models.Model):
    """
    Caja de Control de Estudiante: Maneja ingresos, salidas y cambios de sección.
    """
    class EstadoMatricula(models.TextChoices):
        ACTIVO      = "activo", "Activo"
        RETIRO      = "retirado", "Retirado/Saliente"
        TRASLADO    = "trasladado", "Traslado Interno" # Para cambios de B a A
        REINGRESO   = "reingresante", "Reingresante"

    alumno = models.ForeignKey(PerfilPersona, on_delete=models.PROTECT, related_name="matriculas")
    seccion = models.ForeignKey(Seccion, on_delete=models.PROTECT, related_name="alumnos")
    
    # Registro temporal
    fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_baja = models.DateField(null=True, blank=True)
    
    estado = models.CharField(max_length=15, choices=EstadoMatricula.choices, default=EstadoMatricula.ACTIVO)
    observaciones = models.TextField(blank=True, help_text="Razón de cambio de sección o retiro")

    class Meta:
        db_table = "matricula"
        # Un alumno puede tener varias matrículas en su vida, 
        # pero solo una 'Activa' por periodo (esto se valida en la lógica de Fase 3).

    def __str__(self):
        return f"{self.alumno.user.last_name} en {self.seccion} ({self.estado})"