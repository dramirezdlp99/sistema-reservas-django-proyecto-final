from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Espacios
    path('espacios/', views.lista_espacios, name='lista_espacios'),
    path('espacios/<int:pk>/', views.detalle_espacio, name='detalle_espacio'),
    path('espacios/crear/', views.crear_espacio, name='crear_espacio'),
    path('espacios/<int:pk>/editar/', views.editar_espacio, name='editar_espacio'),
    path('espacios/<int:pk>/eliminar/', views.eliminar_espacio, name='eliminar_espacio'),
    
    # Reservas
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/editar/', views.editar_reserva, name='editar_reserva'),
    path('reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/<int:pk>/confirmar/', views.confirmar_reserva, name='confirmar_reserva'),
    path('historial/', views.historial_reservas, name='historial_reservas'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),
    path('reportes/excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    
    # API
    path('api/calendario/', views.api_reservas_calendario, name='api_reservas_calendario'),
]