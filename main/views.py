from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from accounts.models import User

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