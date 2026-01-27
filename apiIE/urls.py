# apiIE/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Punto de entrada visual (Landing Page)
    path('', include('IEAPI.urls')), 
    
    # 2. Tu exclusivo para el Director
    path('administracion-privada/', admin.site.urls), 
    
    # 3. La API que consumirá tu React/Vue
    path('api/v1/', include('IEAPI.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)