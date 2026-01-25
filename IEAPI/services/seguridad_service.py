# IEAPI/services/seguridad_service.py
from IEAPI.models import AsignacionRol

def validar_vinculo_institucional(persona_id, institucion_id):
    """
    Fase 3: Portero Lógico.
    Verifica si la persona tiene un rol activo antes de dejarlo entrar a la Fase 4.
    """
    return AsignacionRol.objects.filter(
        persona_id=persona_id,
        institucion_id=institucion_id,
        esta_activo=True
    ).exists()