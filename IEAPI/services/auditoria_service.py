# IEAPI/services/auditoria_service.py
from IEAPI.models import LogAuditoria

def registrar_evento_critico(usuario, accion, descripcion):
    """
    Fase 3: Blindaje de Integridad.
    Guarda rastro de acciones como 'Cambio de Nota' o 'Anulación de Pago'.
    """
    return LogAuditoria.objects.create(
        usuario=usuario,
        accion=accion, # Ej: 'UPDATE_NOTA'
        descripcion=descripcion
    )