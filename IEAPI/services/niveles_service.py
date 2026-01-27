from django.db import transaction
from IEAPI.models import InstitucionEducativa, InstitucionNivel, NivelCatalogo

def obtener_niveles_institucion(ie_id):
    """Listar: Trae todos los niveles (activos e inactivos) de la IE."""
    return InstitucionNivel.objects.filter(institucion_id=ie_id).select_related('nivel_tipo')

def gestionar_niveles_institucion(ie_id, codigos_activos):
    """
    Editar/Asignar: Lógica de Sincronización.
    Si el nivel está en 'codigos_activos', se activa.
    Si no está, se marca como inactivo (es_activo=False) en lugar de borrar.
    """
    with transaction.atomic():
        ie = InstitucionEducativa.objects.get(id=ie_id)
        
        # 1. Desactivamos todos los niveles actuales de esta IE
        InstitucionNivel.objects.filter(institucion=ie).update(es_activa=False)
        
        registros = []
        # 2. Activamos o creamos los niveles solicitados
        for codigo in codigos_activos:
            nivel_tipo = NivelCatalogo.objects.get(codigo=codigo)
            inst_nivel, _ = InstitucionNivel.objects.update_or_create(
                institucion=ie,
                nivel_tipo=nivel_tipo,
                defaults={'es_activa': True} # Lo ponemos activo
            )
            registros.append(inst_nivel)
            
        return registros