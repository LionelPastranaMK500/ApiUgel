from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from IEAPI.services.niveles_service import gestionar_niveles_institucion, obtener_niveles_institucion
from IEAPI.serializers.niveles_serializer import InstitucionNivelReadSerializer, AsignarNivelesSerializer

class IEAsignarNivelesView(APIView):
    def get(self, request):
        ie_id = request.query_params.get('institucion_id')
        if not ie_id:
            return Response({"error": "Falta institucion_id"}, status=status.HTTP_400_BAD_REQUEST)
            
        niveles = obtener_niveles_institucion(ie_id)
        serializer = InstitucionNivelReadSerializer(niveles, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Validamos entrada con el serializer que definiste
        serializer = AsignarNivelesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            niveles_procesados = gestionar_niveles_institucion(
                serializer.validated_data['institucion_id'], 
                serializer.validated_data['niveles']
            )
            return Response({
                "mensaje": "Sincronización de niveles completada",
                "activos": len([n for n in niveles_procesados if n.es_activa])
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)