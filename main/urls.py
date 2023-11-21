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
    path("lancar-aula/", LancarAulaView.as_view(), name="launch-class"),
    path("eventos/", EventosView.as_view(), name="events"),
    path("eventos/<int:pk>/", EventoView.as_view(), name="event"),
    path("eventos/<int:pk>/editar/", EditarEvento.as_view(), name="edit-event"),
    path("criar-evento/", CriarEvento.as_view(), name="create-event"),
    path("turmas/", TurmasView.as_view(), name="classes"),
    path('turmas/<int:pk>/', TurmaDetailView.as_view(), name='class'),
    path('turmas/<int:pk>/editar', TurmaUpdateView.as_view(), name='edit-class'),
    path("turmas/criar/", TurmaCreateView.as_view(), name="create-class"),
]