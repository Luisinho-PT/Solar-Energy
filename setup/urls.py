"""
Arquivo de URLs principal do projeto (na pasta 'setup')
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de Login/Logout do Django
    path('contas/', include('django.contrib.auth.urls')),
    
    # Inclui TODAS as urls (loja e clientes) do 'app'
    path('', include('app.urls')), 
]

# Para servir arquivos de mídia (imagens de produtos) em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)