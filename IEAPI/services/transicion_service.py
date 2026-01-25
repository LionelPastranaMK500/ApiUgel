# IEAPI/services/transicion_service.py
from IEAPI.services.promedio_service import calcular_promedio_final
from IEAPI.models import Matricula

def procesar_finalizacion_grado(matricula_id):
    """
    Fase 3: Lógica de Promoción.
    Determina si un alumno pasa al siguiente grado basándose en sus promedios.
    """
    matricula = Matricula.objects.get(pk=matricula_id)
    # 1. Obtenemos todos los cursos de su sección
    cursos = matricula.seccion.curso_set.all()
    
    desaprobados = 0
    for curso in cursos:
        # Usamos el servicio que ya creamos (Reutilización MEFH)
        promedio = calcular_promedio_final(matricula_id, curso.id, "FINAL")
        if promedio < 11: # Lógica estándar peruana
            desaprobados += 1

    # 2. Regla de Negocio: Definir estado final
    if desaprobados == 0:
        matricula.estado_final = 'PROMOVIDO'
    elif desaprobados <= 2:
        matricula.estado_final = 'RECUPERACION'
    else:
        matricula.estado_final = 'REPITENTE'
        
    matricula.save()
    return matricula.estado_final