# IEAPI/models/asignacion_rol.py
from django.db import models
from .usuario import PerfilPersona
from .rol import Rol
from .periodoLectivo import PeriodoLectivo

class PersonalPeriodo(models.Model):
    """
    Caja de Control Humano: Encapsula a todo el personal (admin, servicios, profes) 
    año por año. Soporta cambios y reemplazos mensuales.
    """
    persona = models.ForeignKey(PerfilPersona, on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.PROTECT)
    
    # Especificación del área para servicios públicos o admin
    area_departamento = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Ej: Limpieza, Administración, Matemática"
    )
    
    # Registro de vigencia (Clave para reemplazos a mitad de año)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    
    # Estado para el historial inmutable
    es_titular = models.BooleanField(default=True)
    observaciones_gestion = models.TextField(blank=True, help_text="Motivo de cambio o rotación")

    class Meta:
        db_table = "personal_periodo"
        # La MEFH exige que el código narre su ubicación: 
        # Esta es la Verdad Estructural del personal.