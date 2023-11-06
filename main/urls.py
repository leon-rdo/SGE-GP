from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('meu-perfil/', MeuPerfilView.as_view(), name='my-profile'),
    path("disciplinas/", DisciplinasView.as_view(), name="subjects"),
    path("disciplinas/<int:pk>/desempenho/", DesempenhoView.as_view(), name="performance"),
    path("disciplinas/<int:pk>/atividades/", AtividadesView.as_view(), name="activities"),
    path("disciplinas/<int:pk>/atividades/<int:id>/", AtividadeView.as_view(), name="activity"),
]