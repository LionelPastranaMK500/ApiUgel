# apiIE/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Punto de entrada visual (Landing Page)
    path('', include('IEAPI.urls')), 
    
    # 2. Tu "Modo Dios" exclusivo para el Director
    path('administracion-privada/', admin.site.urls), 
    
    # 3. La API que consumirá tu React/Vue
    path('api/v1/', include('IEAPI.urls')), 
]