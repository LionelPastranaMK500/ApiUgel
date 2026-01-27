from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa, NivelCatalogo, InstitucionNivel

class IENivelesTests(APITestCase):
    """
    Fase 5: Test de Integración para la Activación de Niveles.
    Verifica que la IE pueda vincularse a niveles educativos existentes.
    """
    def setUp(self):
        # 1. Creamos la IE de base
        self.ie = InstitucionEducativa.objects.create(
            nombre="I.E. Prueba",
            codigo_modular="1112223"
        )
        # 2. Creamos los niveles en el catálogo (lo que el servicio buscará)
        NivelCatalogo.objects.create(codigo="PRI", nombre="Primaria")
        NivelCatalogo.objects.create(codigo="SEC", nombre="Secundaria")
        
        self.url = reverse('setup_niveles')

    def test_asignar_niveles_exitosamente(self):
        """Prueba que un POST con niveles válidos cree los registros en MySQL."""
        payload = {
            "institucion_id": self.ie.id,
            "niveles": ["PRI", "SEC"]
        }
        response = self.client.post(self.url, payload, format='json')
        
        # Verificaciones de Certeza Técnica
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InstitucionNivel.objects.filter(institucion=self.ie).count(), 2)
        self.assertTrue(InstitucionNivel.objects.filter(nivel_tipo__codigo="PRI").exists())

    def test_error_nivel_no_existente(self):
        """Verifica que falle si intentamos asignar un nivel que no está en el catálogo."""
        payload = {
            "institucion_id": self.ie.id,
            "niveles": ["UNI"] # 'UNI' no fue creado en el setUp
        }
        response = self.client.post(self.url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)