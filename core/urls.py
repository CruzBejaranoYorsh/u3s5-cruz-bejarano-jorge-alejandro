from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
    path('servicios/<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    path('servicios/<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
]
