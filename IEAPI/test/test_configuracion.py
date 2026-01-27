from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa

class InstitucionIdentidadTests(APITestCase):
    """
    Fase 5 (Validación): Test de Integración para la Identidad de la IE.
    Probamos que el conmutador GET/POST funcione bajo la MEFH.
    """
    def setUp(self):
        # Preparamos la URL usando el nombre que pusimos en urls.py
        self.url = reverse('setup_identidad')
        self.datos_validos = {
            "nombre": "I.E. Los Pioneros",
            "ruc": "20601234567",
            "codigo_modular": "7654321",
            "direccion": "Km 22 Carabayllo"
        }

    def test_crear_institucion_via_post(self):
        """Verifica que el POST cree la IE correctamente."""
        response = self.client.post(self.url, self.datos_validos, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InstitucionEducativa.objects.count(), 1)
        self.assertEqual(InstitucionEducativa.objects.get().nombre, "I.E. Los Pioneros")

    def test_obtener_institucion_via_get(self):
        """Verifica que el GET retorne la info de la IE existente."""
        # Primero creamos una manualmente
        InstitucionEducativa.objects.create(**self.datos_validos)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['codigo_modular'], "7654321")