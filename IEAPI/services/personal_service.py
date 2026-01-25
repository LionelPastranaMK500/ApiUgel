# IEAPI/services/personal_service.py
from django.db import transaction
from IEAPI.models import PersonalPeriodo, AsignacionRol

def proyectar_planilla_personal(periodo_origen_id, periodo_destino_id):
    """
    Fase 3: Continuidad de Planilla con Sincronía de Roles.
    Asegura que el personal proyectado mantenga sus permisos institucionales.
    """
    personal_anterior = PersonalPeriodo.objects.filter(periodo_id=periodo_origen_id)
    periodo_destino_id = periodo_destino_id # ID que viene del DTO
    registros_nuevos = []

    with transaction.atomic():
        for p in personal_anterior:
            # Regla de Negocio: Continuidad para Nombrados o Contratos vigentes
            if p.es_titular or p.fecha_fin is None:
                
                # 1. Sincronía de Rol (Certeza Técnica)
                # Nos aseguramos de que el Rol esté activo en la Institución para este usuario
                AsignacionRol.objects.update_or_create(
                    persona=p.persona,
                    institucion=p.periodo.institucion,
                    rol=p.rol,
                    defaults={'esta_activo': True}
                )

                # 2. Creación del registro en el nuevo periodo
                nuevo_p = PersonalPeriodo.objects.create(
                    persona=p.persona,
                    rol=p.rol,
                    periodo_id=periodo_destino_id,
                    area_departamento=p.area_departamento,
                    # Se asume la fecha de inicio del nuevo periodo para el registro
                    fecha_inicio=p.fecha_inicio, 
                    es_titular=p.es_titular,
                    observaciones_gestion=f"Continuidad automática desde {p.periodo.anio}"
                )
                registros_nuevos.append(nuevo_p)
                
    return registros_nuevos