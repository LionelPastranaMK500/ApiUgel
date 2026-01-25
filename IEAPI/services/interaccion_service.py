# IEAPI/services/interaccion_service.py
from IEAPI.models import DebateTema, Anuncio

def cerrar_debate(debate_id):
    """
    Fase 3: Lógica de Control de Interacción.
    Bloquea un hilo de debate para que no se acepten más posts.
    """
    debate = DebateTema.objects.get(pk=debate_id)
    debate.cerrado = True
    debate.save()
    return debate

def fijar_anuncio_prioritario(anuncio_id):
    """
    Maneja la visibilidad de anuncios importantes en el frontend.
    """
    anuncio = Anuncio.objects.get(pk=anuncio_id)
    anuncio.fijado = True
    anuncio.save()
    return anuncio