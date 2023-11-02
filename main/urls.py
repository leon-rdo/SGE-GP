from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('meu-perfil/', MeuPerfilView.as_view(), name='meu-perfil'),
    path("disciplinas/", DisciplinasView.as_view(), name="disciplinas"),
    path("disciplinas/<int:pk>/desempenho", DesempenhoView.as_view(), name="desempenho"),
    path("disciplinas/<int:pk>/atividades", AtividadesView.as_view(), name="atividades")
]