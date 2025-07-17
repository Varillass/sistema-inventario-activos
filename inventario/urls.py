from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('equipos/', views.equipos_lista, name='equipos_lista'),
    path('equipos/crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/<int:equipo_id>/', views.obtener_equipo, name='obtener_equipo'),
    path('equipos/<int:equipo_id>/editar/', views.editar_equipo, name='editar_equipo'),
    path('equipos/<int:equipo_id>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    path('equipos/exportar-pdf/', views.exportar_equipos_pdf, name='exportar_equipos_pdf'),
    path('equipos/importar-excel/', views.importar_equipos_excel, name='importar_equipos_excel'),
    path('equipos/plantilla-excel/', views.descargar_plantilla_excel, name='descargar_plantilla_excel'),
] 