from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('meu-perfil/', MeuPerfilView.as_view(), name='my-profile'),
    path("disciplinas/", DisciplinasView.as_view(), name="subjects"),
    path("disciplinas/<int:pk>/desempenho/", DesempenhoView.as_view(), name="performance"),
    path("lancar-aula/", LancarAulaView.as_view(), name="launch-class"),
    path('get_students_for_subject/', get_students_for_subject, name='get_students_for_subject'),
    path("professores/", ProfessoresView.as_view(), name="teachers"),
    # Avaliações
    path("avaliacoes/<str:slug>", TestsView.as_view(), name="tests"),
    path("avaliacoes/<str:slug>/abrir/", AbrirAvaliacaoView.as_view(), name="open-test"),
    path("avaliacoes/<int:pk>/", GradesView.as_view(), name="grades"),
    # Eventos
    path("eventos/", EventosView.as_view(), name="events"),
    path("eventos/<int:pk>/", EventoView.as_view(), name="event"),
    path("eventos/<int:pk>/editar/", EditarEvento.as_view(), name="edit-event"),
    path("criar-evento/", CriarEvento.as_view(), name="create-event"),
    path("eventos/<int:pk>/deletar/", DeletarEvento.as_view(), name="delete-event"),
    # Turmas
    path("turmas/", TurmasView.as_view(), name="classes"),
    path('turmas/<int:pk>/', TurmaDetailView.as_view(), name='class'),
    path('turmas/<int:pk>/editar', TurmaUpdateView.as_view(), name='edit-class'),
    path("turmas/criar/", TurmaCreateView.as_view(), name="create-class"),
    # Atividades
    path("disciplinas/<str:slug>/atividades/", ActivityListView.as_view(), name="activities"),
    path("disciplinas/<str:slug>/atividades/<int:pk>/", ActivityDetailView.as_view(), name="activity"),
    path("disciplinas/<str:slug>/atividades/criar/", ActivityCreateView.as_view(), name="create-activity"),
    path("disciplinas/<str:slug>/atividades/<int:pk>/editar/", ActivityUpdateView.as_view(), name="edit-activity"),
    path("disciplinas/<str:slug>/atividades/<int:pk>/deletar/", ActivityDeleteView.as_view(), name="delete-activity"),
]