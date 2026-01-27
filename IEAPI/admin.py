# IEAPI/admin.py
from django.contrib import admin
from .models import (
    InstitucionEducativa, NivelCatalogo, InstitucionNivel, 
    PeriodoLectivo, Grado, Seccion, PerfilPersona, Rol, 
    PersonalPeriodo, Matricula, Asignatura, MallaCurricular, 
    DetalleMalla, Curso, TipoEvaluacion, Evaluacion, 
    EscalaCalificacion, ValorEscala, ComponenteEvaluacion, 
    Calificacion, LogAuditoria
)

# Registros con buscadores para que el Director encuentre todo rápido
@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'seccion', 'estado')
    search_fields = ('alumno__dni', 'alumno__user__last_name')

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'evaluacion', 'valor_numerico', 'valor_literal')
    list_filter = ('evaluacion__curso', 'evaluacion__tipo')

@admin.register(LogAuditoria)
class LogAdmin(admin.ModelAdmin):
    list_display = ('fecha_evento', 'usuario', 'accion')
    readonly_fields = ('fecha_evento', 'usuario', 'accion', 'descripcion')

# Registros estándar para el resto
admin.site.register([
    InstitucionEducativa, NivelCatalogo, InstitucionNivel, PeriodoLectivo, 
    Grado, Seccion, PerfilPersona, Rol, PersonalPeriodo, Asignatura, 
    MallaCurricular, DetalleMalla, Curso, TipoEvaluacion, Evaluacion, 
    EscalaCalificacion, ValorEscala, ComponenteEvaluacion
])