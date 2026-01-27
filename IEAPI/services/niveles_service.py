from django.db import transaction
from IEAPI.models import InstitucionEducativa, InstitucionNivel, NivelCatalogo

def obtener_niveles_institucion(ie_id):
    """Listar: Trae todos los niveles (activos e inactivos) de la IE."""
    return InstitucionNivel.objects.filter(institucion_id=ie_id).select_related('nivel_tipo')

def gestionar_niveles_institucion(ie_id, codigos_activos):
    with transaction.atomic():
        ie = InstitucionEducativa.objects.get(id=ie_id)
        
        InstitucionNivel.objects.filter(institucion=ie).update(es_activo=False)
        
        registros = []
        for codigo in codigos_activos:
            nivel_tipo = NivelCatalogo.objects.get(codigo=codigo)
            inst_nivel, _ = InstitucionNivel.objects.update_or_create(
                institucion=ie,
                nivel_tipo=nivel_tipo,
                defaults={'es_activo': True} # También aquí corregido
            )
            registros.append(inst_nivel)
        return registros