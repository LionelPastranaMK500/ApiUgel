# IEAPI/services/finanzas_service.py
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from IEAPI.models import ObligacionPago

def generar_deuda_estudiante(datos_validados):
    """
    Fase 3: Lógica de Negocio Financiera.
    Aplica reglas según el contexto del colegio (Público/Privado).
    """
    persona = datos_validados.get('persona')
    periodo = datos_validados.get('periodo')
    concepto = datos_validados.get('concepto')
    monto_original = datos_validados.get('monto_original')
    descuento = datos_validados.get('descuento_aplicado', Decimal("0.00"))

    # 1. Obtener contexto de la Institución (Fase 1)
    ie = periodo.institucion 

    # --- REGLA DE NEGOCIO: CONTEXTO PERUANO ---
    
    # Escenario A: Colegio Público (Gratuidad de enseñanza)
    # Algunos solo cobran una cuota única de APAFA o matrícula simbólica.
    if ie.ruc is None or ie.ruc == "": # Asumimos que si no hay RUC es gestión pública directa
        if concepto.es_mensualidad:
            raise ValidationError(f"Error: Los colegios públicos no pueden generar deudas de mensualidad.")
    
    # Escenario B: Colegio Privado
    # Validamos que el descuento no sea un error de digitación (no mayor al 100%)
    if descuento > monto_original:
        raise ValidationError("El descuento no puede superar el monto base del concepto.")

    # 2. Persistencia Atómica
    with transaction.atomic():
        # Aquí se cumple tu lógica: El frontend envía, el servicio valida y sella.
        obligacion = ObligacionPago.objects.create(
            persona=persona,
            periodo=periodo,
            concepto=concepto,
            fecha_vencimiento=datos_validados.get('fecha_vencimiento'),
            monto_original=monto_original,
            descuento_aplicado=descuento,
            esta_pagado=False
        )
    
    return obligacion