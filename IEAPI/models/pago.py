# IEAPI/models/pago.py
from django.db import models
from .usuario import PerfilPersona
from .periodoLectivo import PeriodoLectivo

class ConceptoPago(models.Model):
    """
    Catálogo de cobros: 'Matrícula', 'Mensualidad Abril', 'Derecho de Trámite'.
    """
    nombre = models.CharField(max_length=100)
    monto_base = models.DecimalField(max_digits=10, decimal_places=2)
    es_mensualidad = models.BooleanField(default=True)

    class Meta:
        db_table = "concepto_pago"

class ObligacionPago(models.Model):
    """
    La 'Deuda' generada para una persona. 
    Resuelve el caso de privadas con becas mediante 'descuento_aplicado'.
    """
    persona = models.ForeignKey(PerfilPersona, on_delete=models.PROTECT, related_name="deudas")
    periodo = models.ForeignKey(PeriodoLectivo, on_delete=models.PROTECT)
    concepto = models.ForeignKey(ConceptoPago, on_delete=models.PROTECT)
    
    fecha_vencimiento = models.DateField()
    monto_original = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    esta_pagado = models.BooleanField(default=False)
    fecha_pago_realizado = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "obligacion_pago"
        unique_together = ('persona', 'periodo', 'concepto')

    @property
    def monto_final(self):
        return self.monto_original - self.descuento_aplicado