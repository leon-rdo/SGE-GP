from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from accounts.models import User

class IndexView(TemplateView):
    template_name = "main/index.html"


class MeuPerfilView(TemplateView):
    template_name = "main/meu-perfil.html"


class DisciplinasView(ListView):
    model = Disciplina
    template_name = "main/disciplinas.html"
    context_object_name = "disciplinas"
    

class DesempenhoView(DetailView):
    model = Disciplina
    template_name = "main/desempenho.html"


class AtividadesView(DetailView):
    model = Disciplina
    template_name = "main/atividades.html"
