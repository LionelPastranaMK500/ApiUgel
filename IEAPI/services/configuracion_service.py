from django.db import transaction
from IEAPI.models import InstitucionEducativa

def procesar_identidad_ie(datos_validados):
    """
    Fase 3: Operación atómica de identidad.
    Garantiza integridad total en MySQL.
    """
    with transaction.atomic():
        ie, created = InstitucionEducativa.objects.update_or_create(
            codigo_modular=datos_validados.get('codigo_modular'),
            defaults=datos_validados
        )
        return ie, created

def obtener_detalle_ie():
    """Retorna la única instancia de la institución en el sistema."""
    return InstitucionEducativa.objects.first()