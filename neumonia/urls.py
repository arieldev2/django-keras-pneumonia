from django.urls import path
from .views import (
	PacienteCreateView, PacienteListView, 
	PacienteDetailView, PacienteUpdateView, PacienteDeleteView,
	ClasificacionListView, ClasificacionCreateView,
	ClasificacionDetailView, ClasificacionDeleteView, ClasificacionUpdateView, Home, 
	ClasificacionTodoListView, Search
	)

urlpatterns = [

	path('', Home, name='home'),
	path('paciente/', PacienteListView.as_view(), name='pacientes-list'),
	path('paciente/nuevo/', PacienteCreateView.as_view(), name='paciente-nuevo'),
	
	
	path('paciente/<int:pk>/', PacienteDetailView.as_view(), name='paciente-detalles'),
	path('paciente/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente-editar'),
	path('paciente/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente-eliminar'),

	path('busqueda/', Search, name='search'),


	#path('paciente/expedientes/', ClasificacionTodoListView.as_view(), name='clasificacion-todo'),
	path('paciente/expedientes/', ClasificacionTodoListView.as_view(), name='clasificacion-todo'),
	
	path('paciente/<str:nombre>/', ClasificacionListView.as_view(), name='clasificacion-list'),
	path('paciente/expediente/nuevo/<int:pk>/', ClasificacionCreateView.as_view(), name='clasificacion-nueva'),
	path('paciente/expediente/<int:pk>/', ClasificacionDetailView.as_view(), name='clasificacion-detalles'),
	path('paciente/expediente/editar/<int:pk>/', ClasificacionUpdateView.as_view(), name='clasificacion-editar'),
	path('paciente/expediente/eliminar/<int:pk>/', ClasificacionDeleteView.as_view(), name='clasificacion-eliminar'),



    
]
