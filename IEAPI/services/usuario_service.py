# IEAPI/services/usuario_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from IEAPI.models import PerfilPersona
from .slug_service import generar_slug_unico

def registrar_nuevo_perfil(datos_validados):
    """Fase 3: Creación atómica con generación de Slug."""
    with transaction.atomic():
        perfil = PerfilPersona(**datos_validados)
        perfil.slug = generar_slug_unico(perfil, 'dni')
        perfil.save()
    return perfil

def actualizar_perfil(perfil_id, datos_nuevos):
    """Fase 3: Edición con refresco de Slug si el DNI cambia."""
    perfil = get_object_or_404(PerfilPersona, pk=perfil_id)
    
    for campo, valor in datos_nuevos.items():
        setattr(perfil, campo, valor)
    
    if 'dni' in datos_nuevos:
        perfil.slug = generar_slug_unico(perfil, 'dni')
        
    perfil.save()
    return perfil

def obtener_perfil_por_slug(slug_recibido):
    """Fase 3: Consulta optimizada para el Frontend."""
    return get_object_or_404(
        PerfilPersona.objects.select_related('user'), 
        slug=slug_recibido
    )

def cambiar_estado_usuario(perfil_id, nuevo_estado=False):
    """Fase 3: Control de acceso (Soft Delete)."""
    perfil = get_object_or_404(PerfilPersona.objects.select_related('user'), pk=perfil_id)
    perfil.user.is_active = nuevo_estado
    perfil.user.save()
    return perfil

def verificar_disponibilidad_dni(dni_consulta):
    """Fase 3: Validación de integridad previa."""
    return not PerfilPersona.objects.filter(dni=dni_consulta).exists()