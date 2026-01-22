# IEAPI/models/usuario.py
from django.db import models
from django.contrib.auth.models import User
from .institucionEducativa import InstitucionEducativa

class PerfilPersona(models.Model):
    # Vinculamos al User de Django pero extendemos la identidad peruana
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    dni = models.CharField(max_length=8, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True)
    
    class Meta:
        db_table = "perfil_persona"

class AsignacionRol(models.Model):
    """
    Define qué es una persona dentro de la IE.
    Ejemplos: Estudiante, Docente, Director, Psicólogo, Administrativo.
    """
    persona = models.ForeignKey(PerfilPersona, on_delete=models.CASCADE)
    institucion = models.ForeignKey(InstitucionEducativa, on_delete=models.CASCADE)
    rol_nombre = models.CharField(max_length=50) # 'estudiante', 'docente', etc.
    esta_activo = models.BooleanField(default=True)

    class Meta:
        db_table = "asignacion_rol"
        unique_together = ('persona', 'institucion', 'rol_nombre')