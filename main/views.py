from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from accounts.models import User
from django.views.generic.edit import CreateView

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
    template_name = "main/lancar-aula.html"
    fields = '__all__'