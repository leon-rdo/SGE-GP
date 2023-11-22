from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import *
from .forms import ClassroomForm, TestForm, GradeForm
from django.shortcuts import redirect
from django.contrib import messages


class IndexView(TemplateView):
    template_name = "main/index.html"


class MeuPerfilView(TemplateView):
    template_name = "main/meu-perfil.html"


class DisciplinasView(ListView):
    model = Subject
    template_name = "main/disciplinas.html"
    context_object_name = "subjects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.type == "teacher":
            context["subjects"] = Subject.objects.filter(teacher=self.request.user)
        return context
    
    

class DesempenhoView(DetailView):
    model = Subject
    template_name = "main/desempenho.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grades = Grade.objects.filter(student=self.request.user, test__subject=self.get_object())
        grades_dict = {grade.test.school_test: grade for grade in grades}
        context["grades"] = grades_dict

        # Obter todas as aulas da disciplina
        lessons = Classroom.objects.filter(subject=self.get_object())

        # Obter as faltas do aluno
        absents = [lesson for lesson in lessons if self.request.user not in lesson.attendance_list.all()]
        context["absents"] = absents

        return context
    


class AtividadesView(ListView):
    model = Activity
    template_name = "main/atividades.html"
    

class AtividadeView(DetailView):
    model = Activity
    template_name = "main/atividade.html"
    
    
class LancarAulaView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "main/lancar-aula.html"
    success_url = reverse_lazy("main:subjects")

    def get_form_kwargs(self):
        kwargs = super(LancarAulaView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class TestsView(ListView):
    model = Test
    template_name = "main/avaliacoes.html"
    slug_field = "subject__slug"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tests"] = Test.objects.filter(subject__slug=self.kwargs["slug"])
        context["subject"] = Subject.objects.get(slug=self.kwargs["slug"])
        return context


class AbrirAvaliacaoView(CreateView):
    model = Test
    form_class = TestForm
    template_name = "main/abrir-avalicao.html"

    def get_success_url(self):
        return reverse_lazy("main:tests", kwargs={"slug": self.object.subject.slug})
    
    def get_form_kwargs(self):
        kwargs = super(AbrirAvaliacaoView, self).get_form_kwargs()
        subject = Subject.objects.get(slug=self.kwargs["slug"])
        kwargs.update({'user': self.request.user, 'subject': subject})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject"] = Subject.objects.get(slug=self.kwargs["slug"])
        return context
    
    

class GradesView(DetailView):
    model = Test
    template_name = "main/notas.html"

    def get_success_url(self):
        return reverse_lazy("main:tests", kwargs={"slug": self.object.subject.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = self.object.subject.class_code.enrolled.all()
        student_form_pairs = []
        for student in students:
            grade = student.grade_set.filter(test=self.object).first()
            if grade is None:
                grade = Grade(student=student, test=self.object)
            form = GradeForm(instance=grade)
            student_form_pairs.append((student, form))
        context['student_form_pairs'] = student_form_pairs
        return context

    def post(self, request, *args, **kwargs):   
        self.object = self.get_object()
        students = self.object.subject.class_code.enrolled.all()
        student_form_pairs = []
        for student in students:
            grade = student.grade_set.filter(test=self.object).first()
            if grade is None:
                grade = Grade(student=student, test=self.object)
            form = GradeForm(request.POST or None, prefix=str(student.id), instance=grade)
            if form.has_changed():
                if form.is_valid():
                    form.save()
                else:
                    print(f"Errors for student {student.id}: {form.errors}")
                    messages.error(request, "Erro ao lançar notas.")
                    return self.render_to_response(self.get_context_data(student_form_pairs=student_form_pairs))
            student_form_pairs.append((student, form))

        messages.success(request, "Notas lançadas com sucesso!")
        return redirect(self.get_success_url())
    
    
class EventosView(ListView):
    model = Event
    template_name = "main/eventos.html"
    context_object_name = "events"
    
    
class EventoView(DetailView):
    model = Event
    template_name = "main/evento.html"
    
    
class CriarEvento(CreateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/criar-evento.html"
    success_url = reverse_lazy("main:events")
    

class EditarEvento(UpdateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/criar-evento.html"
    success_url = reverse_lazy("main:events")
    

class TurmasView(ListView):
    model = Class
    template_name = "main/turmas.html"
    context_object_name = "classes"
    

class TurmaDetailView(DetailView):
    model = Class
    template_name = "main/turma.html"
    context_object_name = "class"
    
    
class TurmaUpdateView(UpdateView):
    model = Class
    fields = ['code', 'level', 'academic_year', 'enrolled']
    template_name = "main/editar-turma.html"
    success_url = reverse_lazy("main:classes")


class TurmaCreateView(CreateView):
    model = Class
    fields = ['code', 'level', 'academic_year']
    template_name = "main/criar-turma.html"
    success_url = reverse_lazy("main:classes")


