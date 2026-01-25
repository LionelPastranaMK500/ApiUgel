# IEAPI/services/matricula_service.py
from django.core.exceptions import ValidationError
from django.db import transaction
from IEAPI.models import Matricula

def ejecutar_matricula(datos_validados):
    """
    Fase 3: Lógica de Negocio Pura.
    Enlace con Finanzas: Aquí se podrían inyectar validaciones de deudas previas.
    """
    alumno = datos_validados.get('alumno')
    seccion = datos_validados.get('seccion')
    observaciones = datos_validados.get('observaciones', "")
    ie = seccion.periodo.institucion

    with transaction.atomic():
        # 1. Regla de Negocio: Validación de Vacantes
        if seccion.vacantes <= 0:
            raise ValidationError(f"La sección {seccion} no tiene vacantes.")

        # 2. Regla de Negocio: Contexto Privado (Deudas)
        # Si la IE tiene RUC (es privada), revisamos si el alumno tiene deudas
        if ie.ruc and ie.ruc.strip():
            # Esta es la conexión con el motor financiero (Fase 3)
            tiene_deudas = alumno.deudas.filter(esta_pagado=False).exists()
            if tiene_deudas:
                raise ValidationError("No se puede matricular: El alumno registra deudas pendientes.")

        # 3. Regla de Negocio: Evitar duplicidad activa
        if Matricula.objects.filter(
            alumno=alumno, 
            seccion__periodo=seccion.periodo, 
            estado='activo'
        ).exists():
            raise ValidationError("El alumno ya posee una matrícula activa en este periodo.")

        # 4. Persistencia (Fase 1)
        matricula = Matricula.objects.create(
            alumno=alumno,
            seccion=seccion,
            estado='activo',
            observaciones=observaciones
        )

        # 5. Lógica derivada
        seccion.vacantes -= 1
        seccion.save()

    return matricula