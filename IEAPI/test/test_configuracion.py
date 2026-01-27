import io
from PIL import Image
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa

class InstitucionIdentidadImagenTests(APITestCase):
    """
    Fase 5: Validación de Identidad con soporte de Multimedia.
    Verifica que el servicio y serializer procesen el ImageField.
    """
    def setUp(self):
        self.url = reverse('setup_identidad')
        
        # Creamos una imagen pequeña en memoria para el test
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
        """Prueba que el POST acepte datos multipart con imagen."""
        data = {
            "nombre": "Colegio Tecnológico TKOH",
            "codigo_modular": "9998887",
            "direccion": "Carabayllo km 22",
            "logo": self.logo_simulado
        }
        
        # IMPORTANTE: format='multipart' es necesario para enviar archivos
        response = self.client.post(self.url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ie = InstitucionEducativa.objects.get(codigo_modular="9998887")
        
        # Verificamos que el logo se haya guardado en el path correcto
        self.assertTrue(ie.logo.name.startswith('ie/logos/'))
        self.assertTrue(ie.logo.size > 0)

    def test_obtener_detalle_incluye_url_logo(self):
        """Verifica que el GET devuelva la URL completa del logo."""
        InstitucionEducativa.objects.create(
            nombre="IE Detalle",
            codigo_modular="1234567",
            logo=self.logo_simulado
        )
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF debe devolver la URL del logo
        self.assertIn('logo', response.data)
        self.assertTrue(response.data['logo'].endswith('.png'))