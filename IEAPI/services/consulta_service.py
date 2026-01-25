# IEAPI/services/consulta_service.py
from IEAPI.models import PersonalPeriodo, Matricula

def listar_personal_administracion(periodo_id, **filtros):
    """
    Fase 3: Consulta Quirúrgica de Personal.
    Soporta: rol_id, estado, es_titular, genero, busqueda (nombre/dni).
    """
    qs = PersonalPeriodo.objects.filter(periodo_id=periodo_id).select_related(
        'persona__user', 'rol'
    )
    
    # Filtros Dinámicos
    if filtros.get('rol_id'):
        qs = qs.filter(rol_id=filtros['rol_id'])
    if filtros.get('estado'):
        qs = qs.filter(estado=filtros['estado'])
    if filtros.get('es_titular') is not None:
        qs = qs.filter(es_titular=filtros['es_titular'])
    if filtros.get('genero'):
        qs = qs.filter(persona__genero=filtros['genero'])
    
    # Búsqueda por texto (DNI o Apellido)
    busqueda = filtros.get('q')
    if busqueda:
        from django.db.models import Q
        qs = qs.filter(
            Q(persona__dni__icontains=busqueda) | 
            Q(persona__user__last_name__icontains=busqueda)
        )
        
    return qs.order_by('persona__user__last_name')

def listar_alumnos_administracion(periodo_id, **filtros):
    """
    Fase 3: Consulta Quirúrgica de Alumnos.
    Soporta: seccion_id, estado_matricula, genero, busqueda.
    """
    qs = Matricula.objects.filter(seccion__periodo_id=periodo_id).select_related(
        'alumno__user', 'seccion__grado'
    )
    
    if filtros.get('seccion_id'):
        qs = qs.filter(seccion_id=filtros['seccion_id'])
    if filtros.get('estado_matricula'):
        qs = qs.filter(estado=filtros['estado_matricula'])
    if filtros.get('genero'):
        qs = qs.filter(alumno__genero=filtros['genero'])
        
    busqueda = filtros.get('q')
    if busqueda:
        from django.db.models import Q
        qs = qs.filter(
            Q(alumno__dni__icontains=busqueda) | 
            Q(alumno__user__last_name__icontains=busqueda)
        )
        
    return qs.order_by('alumno__user__last_name')
