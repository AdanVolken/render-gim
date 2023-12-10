from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importamos rutas de nuestras vistas
from .views import (
    home, 
    sesion, 
    cliente, 
    cliente_detail,
    pagos,
    editar_cliente,
    actualizar_cliente,
    descargar_pdf,
    registro

)


urlpatterns = [
    path('', home, name="home"),
    path('sesion/', sesion, name = 'sesion'),
    path('registro/',registro,name="registro"),
    path('cliente/', cliente ,name='cliente'),
    path('cliente/<int:id>/', cliente_detail , name='cliente_detail'),
    path('cliente/editar/<int:id>', editar_cliente, name ='editar_cliente'),
    path('cliente/actualizar/<int:id>', actualizar_cliente, name ='actualizar_cliente'),
    path('cliente/<int:id>/descargar_pdf/', descargar_pdf, name='descargar_pdf'),
    path('pagos/', pagos, name='pagos'),

]    
    
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)