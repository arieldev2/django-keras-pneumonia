from django.shortcuts import render, get_object_or_404
from .models import Clasificacion, Paciente
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


def Home(request):

	title = 'Inicio'

	return render(request, 'neumonia/index.html', {'title':title})


@login_required
def Search(request):
	query = request.GET.get('q')
	
	items = Paciente.objects.filter(Q(nombre__icontains=query) | Q(primer_apellido__icontains=query) | Q(segundo_apellido__icontains=query))
	
	

	context = {
		'items': items,
		
		
	}

	return render(request, 'neumonia/search.html', context)



class PacienteListView(LoginRequiredMixin, ListView):
	model = Paciente
	template_name = 'neumonia/pacientes_list.html'
	context_object_name = 'items'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(PacienteListView, self).get_context_data(**kwargs)
		context['title'] = 'Pacientes'
		return context



class PacienteCreateView(LoginRequiredMixin, CreateView):
	model = Paciente
	fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'edad', 'correo']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(PacienteCreateView, self).get_context_data(**kwargs)
		context['title'] = 'Nuevo Paciente'
		return context

class PacienteDetailView(LoginRequiredMixin, DetailView):
	model = Paciente

	def get_context_data(self, **kwargs):
		context = super(PacienteDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Detalles Paciente'
		return context

class PacienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Paciente
	fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'edad', 'correo']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super(PacienteUpdateView, self).get_context_data(**kwargs)
		context['title'] = 'Actualizar Paciente'
		return context

class PacienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Paciente
	success_url = '/paciente'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super(PacienteDeleteView, self).get_context_data(**kwargs)
		context['title'] = 'Eliminar Paciente'
		return context





#PREDICCION


class ClasificacionTodoListView(LoginRequiredMixin, ListView):
	model = Clasificacion
	template_name = 'neumonia/clasificacion_todo_list.html'
	context_object_name = 'items'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(ClasificacionTodoListView, self).get_context_data(**kwargs)
		context['title'] = 'Expedientes'
		return context


class ClasificacionListView(LoginRequiredMixin, ListView):
	model = Clasificacion
	template_name = 'neumonia/clasificacion_list.html'
	context_object_name = 'items'
	paginate_by = 10

	def get_queryset(self):
		paciente = get_object_or_404(Paciente, nombre=self.kwargs.get('nombre'))
		return Clasificacion.objects.filter(paciente=paciente)

	def get_context_data(self, **kwargs):
		context = super(ClasificacionListView, self).get_context_data(**kwargs)
		context['title'] = 'Expediente Paciente'
		return context

class ClasificacionCreateView(LoginRequiredMixin, CreateView):
	model = Clasificacion
	fields = ['clave_ex', 'img', 'nota']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.paciente = Paciente.objects.get(id=self.kwargs.get('pk'))
		return super().form_valid(form)

	

	def get_context_data(self, **kwargs):
		context = super(ClasificacionCreateView, self).get_context_data(**kwargs)
		context['title'] = 'Nuevo Expediente'
		return context




class ClasificacionDetailView(LoginRequiredMixin, DetailView):
	model = Clasificacion

	def get_context_data(self, **kwargs):
		context = super(ClasificacionDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Detalles Expediente'
		return context

class ClasificacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Clasificacion
	fields = ['paciente', 'clave_ex', 'img', 'nota']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super(ClasificacionUpdateView, self).get_context_data(**kwargs)
		context['title'] = 'Actualizar Expediente'
		return context

class ClasificacionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Clasificacion
	success_url = '/paciente'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def get_context_data(self, **kwargs):
		context = super(ClasificacionDeleteView, self).get_context_data(**kwargs)
		context['title'] = 'Eliminar Expediente'
		return context




