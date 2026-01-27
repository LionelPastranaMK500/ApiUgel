# IEAPI/urls.py
from django.urls import path
from .views.landing_view import IndexView
from .views.configuracion_view import IEConfiguracionView

urlpatterns = [
    # Ruta de bienvenida visual
    path('', IndexView.as_view(), name='index'),
    
    path('setup/institucion/identidad/', IEConfiguracionView.as_view(), name='setup_identidad'),
]