from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from IEAPI.serializers.configuracion_serializer import InstitucionIdentidadSerializer, IEResponseSerializer
from IEAPI.services.configuracion_service import procesar_identidad_ie, obtener_detalle_ie

class IEConfiguracionView(APIView):
    """
    Gestiona la identidad única de la Institución.
    GET: Lee la configuración actual.
    POST: Crea o actualiza los datos maestros.
    """
    def get(self, _):
        ie = obtener_detalle_ie()
        if not ie:
            return Response({"error": "Institución no configurada"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = IEResponseSerializer(ie)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstitucionIdentidadSerializer(data=request.data)
        
        if serializer.is_valid():
            ie, created = procesar_identidad_ie(serializer.validated_data)
            
            return Response({
                "mensaje": "Operación exitosa",
                "id": ie.id,
                "accion": "creado" if created else "actualizado"
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)