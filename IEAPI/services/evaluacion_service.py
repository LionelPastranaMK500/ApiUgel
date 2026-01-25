# IEAPI/services/evaluacion_service.py
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from IEAPI.models import ComponenteEvaluacion

def configurar_esquema_evaluacion(curso, denominacion_periodo, lista_componentes_data):
    """
    Fase 3: Lógica de Configuración de Pesos.
    Permite al profesor definir 'N' tareas con pesos variables.
    Regla: Suma = 100%, No eliminación arbitraria.
    """
    suma_total = Decimal("0.00")
    ids_enviados = []
    
    # 1. Validación de Sumatoria (Certeza Técnica)
    for data in lista_componentes_data:
        peso = Decimal(str(data.get('peso', 0)))
        suma_total += peso
        if data.get('id'):
            ids_enviados.append(data['id'])

    if suma_total != Decimal("100.00"):
        raise ValidationError(f"La suma de pesos debe ser exactamente 100%. Actual: {suma_total}%")

    # 2. Validación de "No Disminución" (Regla de Negocio)
    componentes_actuales = ComponenteEvaluacion.objects.filter(
        curso=curso, 
        denominacion_periodo=denominacion_periodo,
        activo=True
    )
    
    # Si intentan enviar menos tareas de las que ya existen
    if componentes_actuales.count() > len(lista_componentes_data):
        # Aquí podrías añadir un check de 'permiso_especial'
        raise ValidationError("No se permite eliminar tareas existentes. Solo puedes aumentar o ajustar porcentajes.")

    # 3. Persistencia Atómica
    with transaction.atomic():
        for data in lista_componentes_data:
            ComponenteEvaluacion.objects.update_or_create(
                id=data.get('id'), # Si tiene ID, actualiza; si no, crea
                curso=curso,
                denominacion_periodo=denominacion_periodo,
                defaults={
                    'nombre': data['nombre'],
                    'peso': Decimal(str(data['peso'])),
                    'tipo': data['tipo'], # FK a TipoEvaluacion
                    'activo': True
                }
            )