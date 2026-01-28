from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from IEAPI.models import InstitucionEducativa, PeriodoLectivo

class PeriodoLectivoFlowTests(APITestCase):
    """Fase 5: Validación del Ciclo de Vida del Periodo Lectivo."""

    def setUp(self):
        # Creamos la IE base con un código modular único
        self.ie = InstitucionEducativa.objects.create(
            nombre="Colegio de Prueba Periodos",
            codigo_modular="1000001",
            direccion="Carabayllo"
        )
        self.url = reverse('setup_periodos')

    def test_flujo_completo_periodo_lectivo(self):
        # --- 1. CREAR PERIODO 2025 ---
        data_2025 = {
            "institucion_id": self.ie.id,
            "anio": 2025,
            "fecha_inicio": "2025-03-01",
            "fecha_fin": "2025-12-20",
            "es_periodo_actual": True
        }
        response_create = self.client.post(self.url, data_2025, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        id_2025 = response_create.data['id']

        # --- 2. EDITAR PERIODO 2025 (Cambio de fecha de fin) ---
        data_2025_edit = data_2025.copy()
        data_2025_edit["fecha_fin"] = "2025-12-30"
        response_edit = self.client.post(self.url, data_2025_edit, format='json')
        self.assertEqual(response_edit.status_code, status.HTTP_200_OK)
        
        # Verificar cambio en DB
        self.assertEqual(PeriodoLectivo.objects.get(id=id_2025).fecha_fin.isoformat(), "2025-12-30")

        # --- 3. CREAR PERIODO 2026 (Y verificar alternancia de 'actual') ---
        data_2026 = {
            "institucion_id": self.ie.id,
            "anio": 2026,
            "fecha_inicio": "2026-03-01",
            "fecha_fin": "2026-12-15",
            "es_periodo_actual": True
        }
        self.client.post(self.url, data_2026, format='json')
        
        # El 2025 ya no debe ser el actual
        p_2025 = PeriodoLectivo.objects.get(id=id_2025)
        self.assertFalse(p_2025.es_periodo_actual)

        # --- 4. LISTAR PERIODOS (Formato Simple) ---
        # GET /setup/institucion/periodos/?institucion_id=X
        response_list = self.client.get(f"{self.url}?institucion_id={self.ie.id}")
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 2)
        # Verificamos que no trae fecha_inicio en el listado (Serializer Simple)
        self.assertNotIn('fecha_inicio', response_list.data[0])

        # --- 5. DETALLE DE UN PERIODO ---
        # GET /setup/institucion/periodos/?id=X
        response_detail = self.client.get(f"{self.url}?id={id_2025}")
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        # Aquí sí debe venir la fecha (Serializer Full)
        self.assertIn('fecha_inicio', response_detail.data)
        self.assertEqual(response_detail.data['anio'], 2025)