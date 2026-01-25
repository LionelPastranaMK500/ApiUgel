# IEAPI/services/configuracion_service.py
from django.db import transaction
from IEAPI.models import InstitucionEducativa, InstitucionNivel, NivelCatalogo

def inicializar_institucion_maestra(datos_ie, codigos_niveles):
    """
    Fase 3: Génesis. Configura la IE por primera vez.
    Eliminamos 'created' por ser código muerto.
    """
    with transaction.atomic():
        # 1. Identidad Inmutable
        ie, _ = InstitucionEducativa.objects.update_or_create(
            codigo_modular=datos_ie.get('codigo_modular'),
            defaults=datos_ie
        )

        # 2. Activación de niveles
        for cod in codigos_niveles:
            nivel_tipo = NivelCatalogo.objects.get(codigo=cod)
            InstitucionNivel.objects.get_or_create(
                institucion=ie,
                nivel_tipo=nivel_tipo
            )
            
    return ie