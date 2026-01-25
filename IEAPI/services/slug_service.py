# IEAPI/services/slug_service.py
from django.utils.text import slugify

def generar_slug_unico(instancia, campo_origen, campo_destino='slug'):
    """
    Fase 3: Utilidad de Identidad.
    Crea un slug amigable basado en un nombre (ej: 'juan-perez-123').
    """
    valor_base = getattr(instancia, campo_origen)
    slug = slugify(valor_base)
    
    # Verificamos si ya existe para evitar colisiones
    Klass = instancia.__class__
    exists = Klass.objects.filter(**{campo_destino: slug}).exclude(id=instancia.id).exists()
    
    if exists:
        # Si existe, le pegamos el ID para asegurar unicidad
        slug = f"{slug}-{instancia.id}"
        
    return slug