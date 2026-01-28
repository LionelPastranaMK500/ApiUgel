# IEAPI/urls.py
from django.urls import path
from .views.landing_view import IndexView
from .views.configuracion_view import IEConfiguracionView
from .views.niveles_view import IEAsignarNivelesView
from .views.periodo_view import PeriodoLectivoView

urlpatterns = [
    # Ruta de bienvenida visual
    path('', IndexView.as_view(), name='index'),
    
    # Identidad (GET: Detalle / POST: Crear-Editar)
    path('setup/institucion/identidad/', IEConfiguracionView.as_view(), name='setup_identidad'),
    
    # Niveles (GET: Listar estado / POST: Sincronizar activos)
    path('setup/institucion/niveles/', IEAsignarNivelesView.as_view(), name='setup_niveles'),
    
    # Periodos Lectivos (GET: Listar,detalle / POST: Crear-Editar)
    path('setup/institucion/periodos/', PeriodoLectivoView.as_view(), name='setup_periodos'),

]