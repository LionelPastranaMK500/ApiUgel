from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from IEAPI.serializers.periodo_serializers import PeriodoSimpleSerializer, PeriodoFullSerializer
from IEAPI.services.periodo_service import listar_periodos_por_ie, procesar_periodo_lectivo, obtener_periodo_detalle

class PeriodoLectivoView(APIView):
    def get(self, request):
        # 1. Si viene un 'id', devolvemos el DETALLE
        periodo_id = request.query_params.get('id')
        if periodo_id:
            periodo = obtener_periodo_detalle(periodo_id)
            if not periodo:
                return Response({"error": "Periodo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response(PeriodoFullSerializer(periodo).data)

        # 2. Si no viene ID pero sí 'institucion_id', devuelvo LISTADO
        ie_id = request.query_params.get('institucion_id')
        if ie_id:
            periodos = listar_periodos_por_ie(ie_id)
            return Response(PeriodoSimpleSerializer(periodos, many=True).data)

        return Response({"error": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Crear o Editar (Fase 3: Procesar)"""
        ie_id = request.data.get('institucion_id')
        serializer = PeriodoFullSerializer(data=request.data)
        
        if serializer.is_valid():
            periodo, created = procesar_periodo_lectivo(ie_id, serializer.validated_data)
            return Response({
                "mensaje": "Periodo procesado",
                "id": periodo.id,
                "accion": "creado" if created else "actualizado"
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)