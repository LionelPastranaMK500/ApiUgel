from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa, NivelCatalogo, InstitucionNivel

class IENivelesTests(APITestCase):
    def setUp(self):
        # 1. IE con código modular único para evitar conflictos
        self.ie = InstitucionEducativa.objects.create(
            nombre="I.E. Los Pioneros del Km22",
            codigo_modular="7770001",
            direccion="Carabayllo"
        )
        # 2. Poblamos el catálogo (El servicio los necesita para el .get())
        NivelCatalogo.objects.get_or_create(codigo="PRI", defaults={"nombre": "Primaria"})
        NivelCatalogo.objects.get_or_create(codigo="SEC", defaults={"nombre": "Secundaria"})
        NivelCatalogo.objects.get_or_create(codigo="SUP", defaults={"nombre": "Superior"})
        
        self.url = reverse('setup_niveles')

    def test_sincronizar_niveles_exitosamente(self):
        """Verifica la activación de niveles y el status 200."""
        payload = {
            "institucion_id": self.ie.id,
            "niveles": ["PRI", "SEC"]
        }
        response = self.client.post(self.url, payload, format='json')
        
        # SI FALLA, ESTO TE MOSTRARÁ EL ERROR REAL EN LA TERMINAL
        if response.status_code == 400:
            print(f"\n DEBUG ERROR: {response.data}") 
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_desactivacion_logica(self):
        """Verifica que el update_or_create apague niveles no enviados."""
        # Primero aseguramos que Superior existe y está activo
        nivel_sup = NivelCatalogo.objects.get(codigo="SUP")
        InstitucionNivel.objects.create(institucion=self.ie, nivel_tipo=nivel_sup, es_activo=True)
        
        # Sincronizamos enviando solo Primaria
        self.client.post(self.url, {"institucion_id": self.ie.id, "niveles": ["PRI"]}, format='json')
        
        superior = InstitucionNivel.objects.get(institucion=self.ie, nivel_tipo__codigo="SUP")
        self.assertFalse(superior.es_activo) # Certeza: desactivado lógicamente