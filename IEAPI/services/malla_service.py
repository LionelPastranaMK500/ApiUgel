# IEAPI/services/malla_service.py
from django.db import transaction
from django.core.exceptions import ValidationError
from IEAPI.models import MallaCurricular, DetalleMalla

def evolucionar_malla(malla_origen_id, nuevo_anio):
    """
    Clona la malla de 2025 para que sea la base de 2026.
    Sale como 'es_vigente = False' (Borrador) para permitir edición.
    """
    malla_origen = MallaCurricular.objects.get(pk=malla_origen_id)
    detalles_origen = DetalleMalla.objects.filter(malla=malla_origen)

    with transaction.atomic():
        nueva_malla = MallaCurricular.objects.create(
            nombre=f"{malla_origen.nombre} - {nuevo_anio}",
            nivel=malla_origen.nivel,
            anio_aprobacion=nuevo_anio,
            es_vigente=False # Estado: BORRADOR
        )

        for d in detalles_origen:
            DetalleMalla.objects.create(
                malla=nueva_malla,
                grado=d.grado,
                asignatura=d.asignatura,
                horas_semanales=d.horas_semanales
            )
    return nueva_malla

def validar_y_congelar_malla(malla_id):
    """
    Sella la malla. Una vez vigente, el sistema impedirá cambios en los Cursos.
    """
    malla = MallaCurricular.objects.get(pk=malla_id)
    # Aquí iría lógica de "Solo el Director puede firmar" (Fase 3.5)
    malla.es_vigente = True
    malla.save()
    return malla

def agregar_curso_a_malla_vigente(malla_id, datos_curso):
    """
    Regla de Negocio: Bloquea ediciones si la malla ya está firmada por el Director.
    """
    malla = MallaCurricular.objects.get(pk=malla_id)
    
    if malla.es_vigente:
        # Aquí es donde el sistema se pone "Mounstro"
        raise ValidationError("Certeza Técnica: No se pueden añadir cursos a una malla ya validada y vigente.")
    
    # Si no es vigente (borrador), se permite la creación
    return DetalleMalla.objects.create(malla=malla, **datos_curso)