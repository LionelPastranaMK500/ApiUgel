# IEAPI/services/promedio_service.py
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Avg
from IEAPI.models import Calificacion, ComponenteEvaluacion

def calcular_promedio_final(matricula_id, curso_id, denominacion_periodo):
    """
    Fase 3: Motor de Cálculo Ponderado.
    Calcula la nota final basándose en el esquema de pesos del profesor.
    """
    componentes = ComponenteEvaluacion.objects.filter(
        curso_id=curso_id,
        denominacion_periodo=denominacion_periodo,
        activo=True
    )

    nota_final = Decimal("0.00")
    
    for comp in componentes:
        # Buscamos la calificación específica para este componente (tarea)
        # Nota: Aquí asumimos que Evaluacion se vincula al Componente por nombre/tipo
        notas_qs = Calificacion.objects.filter(
            matricula_id=matricula_id,
            evaluacion__curso_id=curso_id,
            evaluacion__tipo=comp.tipo
        )

        if notas_qs.exists():
            # Si hay varias notas para un tipo (ej. sub-tareas), las promedia
            avg_componente = notas_qs.aggregate(Avg('valor_numerico'))['avg_nota'] or Decimal("0")
            
            # Aplicamos el peso definido por el profesor
            nota_final += (avg_componente * comp.peso) / Decimal("100.00")

    return nota_final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)