# IEAPI/views/landing_view.py
from django.views.generic import TemplateView

class IndexView(TemplateView):
    """
    Fase 4: Punto de entrada visual.
    Muestra la bienvenida a la API.
    """
    template_name = "index.html"