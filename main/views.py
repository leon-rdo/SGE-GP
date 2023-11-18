from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from django.views.generic.edit import CreateView
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