from django.db import transaction
from IEAPI.models import PeriodoLectivo, InstitucionEducativa

def listar_periodos_por_ie(ie_id):
    """Listar: Todos los años escolares de la IE."""
    return PeriodoLectivo.objects.filter(institucion_id=ie_id).order_by('-anio')

def obtener_periodo_detalle(periodo_id):
    """Trae un periodo específico por su ID."""
    try:
        return PeriodoLectivo.objects.get(id=periodo_id)
    except PeriodoLectivo.DoesNotExist:
        return None

def procesar_periodo_lectivo(ie_id, datos_periodo):
    """
    Crear/Editar: Operación atómica para gestionar el año escolar.
    Si se marca como 'es_periodo_actual', los demás se apagan automáticamente.
    """
    with transaction.atomic():
        ie = InstitucionEducativa.objects.get(id=ie_id)
        es_actual = datos_periodo.get('es_periodo_actual', False)

        # Si este periodo será el actual, desactivamos el flag en los otros
        if es_actual:
            PeriodoLectivo.objects.filter(institucion=ie).update(es_periodo_actual=False)

        periodo, created = PeriodoLectivo.objects.update_or_create(
            institucion=ie,
            anio=datos_periodo.get('anio'),
            defaults={
                'fecha_inicio': datos_periodo.get('fecha_inicio'),
                'fecha_fin': datos_periodo.get('fecha_fin'),
                'es_periodo_actual': es_actual
            }
        )
        return periodo, created
    
    