import io
from PIL import Image
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa

class InstitucionConfiguracionTests(APITestCase):
    def setUp(self):
        self.url = reverse('setup_identidad')
        # Generamos imagen en memoria para el test
        file_payload = io.BytesIO()
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(file_payload, format='PNG')
        file_payload.seek(0)
        self.logo_simulado = SimpleUploadedFile(
            name='test_logo.png',
            content=file_payload.read(),
            content_type='image/png'
        )

    def test_crear_ie_con_logo_exitosamente(self):
        """Usa un código modular único para evitar choques en DB."""
        codigo_modular_test = "9000001"
        data = {
            "nombre": "I.E. Tecnologia Master",
            "codigo_modular": codigo_modular_test,
            "direccion": "Av. Peru 123",
            "logo": self.logo_simulado
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verificamos la persistencia en la BD de pruebas
        self.assertTrue(InstitucionEducativa.objects.filter(codigo_modular=codigo_modular_test).exists())

    def test_obtener_detalle_ie(self):
        """Verifica que el GET traiga la única IE configurada."""
        InstitucionEducativa.objects.create(
            nombre="IE Lectura Test",
            codigo_modular="8000001",
            direccion="Direccion Test"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)