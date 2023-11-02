from django.views.generic import TemplateView
from accounts.models import User

class IndexView(TemplateView):
    template_name = "main/disciplinas.html"
    
class MeuPerfilView(TemplateView):
    template_name = "main/meu-perfil.html"