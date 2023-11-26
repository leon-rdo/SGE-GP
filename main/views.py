from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ClassroomForm, TestForm, GradeForm
from accounts.models import User
from .models import *


class IndexView(TemplateView):
    template_name = "main/index.html"


class MeuPerfilView(LoginRequiredMixin, TemplateView):
    template_name = "main/meu-perfil.html"


class DisciplinasView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "main/disciplinas.html"
    context_object_name = "subjects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.type == "teacher":
            context["subjects"] = Subject.objects.filter(teacher=self.request.user)
        elif self.request.user.type == "student":
            student = self.request.user
            student_class = Class.objects.get(enrolled=student)
            context["subjects"] = Subject.objects.filter(class_code=student_class)
        return context
    
    
class DesempenhoView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Subject
    template_name = "main/desempenho.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grades = Grade.objects.filter(student=self.request.user, test__subject=self.get_object())
        grades_dict = {grade.test.school_test: grade for grade in grades}
        context["grades"] = grades_dict
        
        # Calcula a média do aluno
        # Passo 1: Verifique se todas as notas estão presentes
        if all(grade in grades_dict for grade in ['1', '2', '3', '4']):
            # Passo 2: Calcule a média das primeiras 4 notas
            average = sum(grades_dict[grade].grade for grade in ['1', '2', '3', '4']) / 4

            # Passo 3: Verifique se há uma nota para a prova final
            if 'PF' in grades_dict:
                # Passo 4: Adicione a nota da prova final à média calculada e divida por 2
                average = (average + grades_dict['PF'].grade) / 2

            # Passo 5: Armazene o resultado na variável 'average'
            context["average"] = average

        # Get all the lessons of the subject
        lessons = Classroom.objects.filter(subject=self.get_object())

        # Get the student's absences
        absents = [lesson for lesson in lessons if self.request.user not in lesson.attendance_list.all()]
        context["absents"] = absents

        return context
    
    def test_func(self):    
        return self.request.user.type == "student"
    

def get_students_for_subject(request):
    subject = Subject.objects.get(id=request.GET.get('subject', None))
    students = subject.class_code.enrolled.all() | subject.academic_probation.all()
    student_list = [{'id': student.id, 'name': str(student)} for student in students]
    return JsonResponse(student_list, safe=False)


class LancarAulaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = "main/lancar-aula.html"
    success_url = reverse_lazy("main:subjects")

    def get_form_kwargs(self):
        kwargs = super(LancarAulaView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def test_func(self):    
        return self.request.user.type == "teacher" or self.request.user.type == "coordinator"
    

class ProfessoresView(LoginRequiredMixin, ListView):
    model = User
    template_name = "main/professores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.type == "coordinator" or self.request.user.type == "teacher":
            context["teachers"] = User.objects.filter(type="teacher")
        else:
            student_class = Class.objects.get(enrolled=self.request.user)
            subjects = Subject.objects.filter(class_code=student_class)
            context["subjects"] = subjects
        return context


class TestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Test
    template_name = "main/avaliacoes/avaliacoes.html"
    slug_field = "subject__slug"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tests"] = Test.objects.filter(subject__slug=self.kwargs["slug"])
        context["subject"] = Subject.objects.get(slug=self.kwargs["slug"])
        return context
    
    def test_func(self):    
        teacher = get_object_or_404(Subject, slug=self.kwargs['slug']).teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"


class AbrirAvaliacaoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = "main/avaliacoes/abrir-avalicao.html"

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
    
    def test_func(self):    
        teacher = get_object_or_404(Subject, slug=self.kwargs['slug']).teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"
    

class GradesView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Test
    template_name = "main/avaliacoes/notas.html"
    
    def test_func(self):    
        teacher = get_object_or_404(Test, pk=self.kwargs['pk']).subject.teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"

    def get_success_url(self):
        return reverse_lazy("main:tests", kwargs={"slug": self.object.subject.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = self.object.subject.class_code.enrolled.all()
        student_form_pairs = []
        for student in students:
            grade = student.grade_set.filter(test=self.object).first()
            if grade is not None:
                grade.grade = str(grade.grade).replace(',', '.')
                grade.save()
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
    
    
class EventosView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "main/eventos/eventos.html"
    context_object_name = "events"
    
    
class EventoView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "main/eventos/evento.html"
    
    
class CriarEvento(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/eventos/criar-evento.html"
    success_url = reverse_lazy("main:events")
    
    def test_func(self):    
        return self.request.user.type == "coordinator"
    

class EditarEvento(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['image', 'title', 'description', 'date_time']
    template_name = "main/eventos/criar-evento.html"
    success_url = reverse_lazy("main:events")
    
    def test_func(self):    
        return self.request.user.type == "coordinator"
    
    
class DeletarEvento(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event

    def test_func(self):    
        return self.request.user.type == "coordinator"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("main:events")
    

class TurmasView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Class
    template_name = "main/turmas/turmas.html"
    context_object_name = "classes"
    
    def test_func(self):    
        return self.request.user.type == "coordinator"
    

class TurmaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Class
    template_name = "main/turmas/turma.html"
    context_object_name = "class"
    
    def test_func(self):    
        return self.request.user.type == "coordinator"
    
    
class TurmaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Class
    fields = ['code', 'level', 'academic_year', 'enrolled']
    template_name = "main/turmas/editar-turma.html"
    success_url = reverse_lazy("main:classes")
    
    def test_func(self):    
        return self.request.user.type == "coordinator"


class TurmaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Class
    fields = ['code', 'level', 'academic_year']
    template_name = "main/turmas/criar-turma.html"
    success_url = reverse_lazy("main:classes")
    
    def test_func(self):    
        return self.request.user.type == "coordinator"


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "main/atividades/activities.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(slug=self.kwargs["slug"])
        context["subject"] = subject 
        context["activities"] = Activity.objects.filter(subject=subject)
        return context


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = "main/atividades/activity.html"
    context_object_name = "activity"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(slug=self.kwargs["slug"])
        context["subject"] = subject
        context["has_permition"] = self.request.user == subject.teacher or self.request.user.type == "coordinator"
        return context


class ActivityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Activity
    fields = ['title', 'prompt', 'image', 'delivery_date']
    template_name = "main/atividades/create-activity.html"
    
    def test_func(self):    
        teacher = get_object_or_404(Subject, slug=self.kwargs['slug']).teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"
    
    def get_success_url(self):
        return reverse_lazy("main:activities", kwargs={"slug": self.kwargs["slug"]})
    
    def form_valid(self, form):
        subject_slug = self.kwargs['slug']
        subject = get_object_or_404(Subject, slug=subject_slug)
        form.instance.subject = subject
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject"] = Subject.objects.get(slug=self.kwargs["slug"])
        return context 


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    fields = ['title', 'prompt', 'image', 'delivery_date']
    template_name = "main/atividades/edit-activity.html"
    
    def test_func(self):    
        teacher = get_object_or_404(Subject, slug=self.kwargs['slug']).teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subject"] = Subject.objects.get(slug=self.kwargs["slug"])
        return context 

    def get_success_url(self):
        return reverse_lazy("main:activities", kwargs={"slug": self.kwargs["slug"]})


class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Activity
        
    def test_func(self):    
        teacher = get_object_or_404(Subject, slug=self.kwargs['slug']).teacher
        return self.request.user == teacher or self.request.user.type == "coordinator"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("main:activities", kwargs={"slug": self.kwargs["slug"]})