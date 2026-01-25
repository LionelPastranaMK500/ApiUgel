# IEAPI/services/reporte_service.py
from IEAPI.models import Matricula

def obtener_estadisticas_seccion(seccion_id):
    """
    Fase 3: Lógica de Análisis.
    Devuelve un resumen de la situación de una sección.
    """
    qs = Matricula.objects.filter(seccion_id=seccion_id)
    
    total = qs.count()
    activos = qs.filter(estado='activo').count()
    retirados = qs.filter(estado='retirado').count()
    
    return {
        "total_alumnos": total,
        "alumnos_activos": activos,
        "alumnos_retirados": retirados,
        "porcentaje_desercion": (retirados / total * 100) if total > 0 else 0
    }