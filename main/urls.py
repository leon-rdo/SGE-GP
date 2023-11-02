from django.urls import path
from .views import IndexView, MeuPerfilView

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('meu-perfil/', MeuPerfilView.as_view(), name='meu-perfil'),
]