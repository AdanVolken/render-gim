from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# funciones usadasa en las vistas
from .views import (
    rutina,
    rutina_detail,
    ejercicios,
    agregar_ejercicio,

    editar_ejercicio,
    actualizar_ejercicio,
    editar_rutina,
    actualizar_rutina,  
)


urlpatterns = [
    path('', rutina , name = 'rutina'),
    path('<int:id>/', rutina_detail, name = 'rutina_id'),
    path('ejercicios/', ejercicios, name = 'ejercicios'),
    path('ejercicios/agregar/',agregar_ejercicio, name= 'agregar_ejercicio'),
    path('ejercicios/editar/<int:id_ejercicio>/', editar_ejercicio, name='editar_ejercicio'),
    path('ejercicios/actualizar/<int:id_ejercicio>/', actualizar_ejercicio, name='actualizar_ejercicio'),
    path('editar/<int:id_rutina>/', editar_rutina, name='editar_rutina'),
    path('actualizar/<int:id_rutina>/', actualizar_rutina, name='actualizar_rutina'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)