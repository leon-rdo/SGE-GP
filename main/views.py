from django.views.generic import TemplateView, DetailView, ListView
from .models import *
from accounts.models import User

class IndexView(TemplateView):
    template_name = "main/index.html"
    
class MeuPerfilView(TemplateView):
    template_name = "main/meu-perfil.html"

class DisciplinasView(ListView):
    model = Disciplina
    template_name = "main/disciplinas.html"
