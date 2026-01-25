# IEAPI/serializers/pago_serializers.py
from rest_framework import serializers
from IEAPI.models import ConceptoPago, ObligacionPago

class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoPago
        fields = ['id', 'nombre', 'monto_base', 'es_mensualidad']

class ObligacionPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligacionPago
        fields = [
            'id', 'persona', 'periodo', 'concepto', 
            'fecha_vencimiento', 'monto_original', 
            'descuento_aplicado', 'esta_pagado'
        ]