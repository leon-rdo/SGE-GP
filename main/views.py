from django.views.generic import TemplateView, DetailView
from .models import *

class IndexView(TemplateView):
    template_name = "main/disciplinas.html"

class DisciplinasView(DetailView):
    model = Disciplina
    template_name = "disciplinas.html"
