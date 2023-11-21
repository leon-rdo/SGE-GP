from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import ClassroomForm


class IndexView(TemplateView):
    template_name = "main/index.html"


class MeuPerfilView(TemplateView):
    template_name = "main/meu-perfil.html"


class DisciplinasView(ListView):
    model = Subject
    template_name = "main/disciplinas.html"
    context_object_name = "subjects"
    

class DesempenhoView(DetailView):
    model = Subject
    template_name = "main/desempenho.html"


class AtividadesView(ListView):
    model = Activity
    template_name = "main/atividades.html"
    

class AtividadeView(DetailView):
    model = Activity
    template_name = "main/atividade.html"
    
    
class LancarAulaView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "main/lancar-aula.html"
    success_url = reverse_lazy("main:subjects")

    def get_form_kwargs(self):
        kwargs = super(LancarAulaView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    
class EventosView(ListView):
    model = Event
    template_name = "main/eventos.html"
    context_object_name = "events"
    
    
class EventoView(DetailView):
    model = Event
    template_name = "main/evento.html"
    
    
class CriarEvento(CreateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/criar-evento.html"
    success_url = reverse_lazy("main:events")
    

class EditarEvento(UpdateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/criar-evento.html"
    success_url = reverse_lazy("main:events")
    

class TurmasView(ListView):
    model = Class
    template_name = "main/turmas.html"
    context_object_name = "classes"
    

class TurmaDetailView(DetailView):
    model = Class
    template_name = "main/turma.html"
    context_object_name = "class"
    
    
class TurmaUpdateView(UpdateView):
    model = Class
    fields = ['code', 'level', 'academic_year', 'enrolled']
    template_name = "main/editar-turma.html"
    success_url = reverse_lazy("main:classes")


class TurmaCreateView(CreateView):
    model = Class
    fields = ['code', 'level', 'academic_year']
    template_name = "main/criar-turma.html"
    success_url = reverse_lazy("main:classes")


