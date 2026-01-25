# IEAPI/services/asistencia_service.py
from django.db import transaction
from IEAPI.models import AsistenciaAlumno

def registrar_asistencia_seccion(fecha, lista_datos_validados):
    """
    Fase 3: Lógica de Negocio Grupal.
    Procesa el registro masivo de asistencia.
    Flexibilidad MEFH: Registra el 'hecho' sin depender de un calendario rígido.
    """
    registros_finales = []

    with transaction.atomic():
        for data in lista_datos_validados:
            matricula = data.get('matricula')
            estado = data.get('estado')
            observacion = data.get('observacion', "")

            # update_or_create permite corregir errores el mismo día (Certeza Técnica)
            obj, _ = AsistenciaAlumno.objects.update_or_create(
                matricula=matricula,
                fecha=fecha,
                defaults={
                    'estado': estado, 
                    'observacion': observacion
                }
            )
            registros_finales.append(obj)
            
    return registros_finales