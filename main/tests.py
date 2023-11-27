from datetime import datetime
from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from .models import Subject, Classroom, Test, Grade, Event, Class, Activity
from .forms import ClassroomForm, TestForm, GradeForm


User = get_user_model()


# Teste para o modelo Subject
class SubjectModelTest(TestCase):
    # Configuração inicial para os testes deste modelo
    def setUp(self):
        # Cria um objeto Subject para ser usado nos testes
        self.subject = Subject.objects.create(
            name="Math",
            syllabus="Algebra and Geometry",
            class_code=Class.objects.create(code="101", level="1", academic_year=2022),
            teacher=User.objects.create(username="teacher1", password="password")
        )

    # Teste para verificar se o slug é criado corretamente
    def test_slug_creation(self):
        # Verifica se o slug do objeto Subject é igual ao esperado
        self.assertEqual(self.subject.slug, "math-101-1-2022")


# Teste para o modelo Classroom
class ClassroomModelTest(TestCase):
    # Configuração inicial para os testes deste modelo
    def setUp(self):
        # Cria um objeto Classroom e dois objetos User (alunos) para serem usados nos testes
        self.classroom = Classroom.objects.create(
            subject=Subject.objects.create(name="Math", syllabus="Algebra and Geometry", class_code=Class.objects.create(code="101", level="1", academic_year=2022), teacher=User.objects.create(username="teacher1", password="password")),
            class_code=Class.objects.create(code="102", level="2", academic_year=2022),
            date="2022-01-01",
            class_diary="Today we learned about algebra."
        )
        self.student1 = User.objects.create(username="student1", password="password")
        self.student2 = User.objects.create(username="student2", password="password")
        # Adiciona os dois alunos à turma e o primeiro aluno à lista de presença da aula
        self.classroom.class_code.enrolled.add(self.student1, self.student2)
        self.classroom.attendance_list.add(self.student1)

    # Teste para verificar se o método get_absent_students funciona corretamente
    def test_get_absent_students(self):
        # Verifica se a lista de alunos ausentes retornada pelo método é igual à esperada
        self.assertEqual(self.classroom.get_absent_students(), {self.student2})
        

class TestForms(TestCase):
    def setUp(self):
        # Configuração inicial do teste. É executado antes de cada método de teste.
        # Cria um usuário professor para os testes
        self.teacher = User.objects.create_user(username='testteacher', password='12345', type='teacher')
        # Cria uma matéria para os testes
        self.subject = Subject.objects.create(name='Math', teacher=self.teacher, class_code=Class.objects.create(code='1A', academic_year='2022'), slug='required-slug')
        # Cria alguns alunos para os testes
        self.student1 = User.objects.create_user(username='student1', password='12345', type='student')
        self.student2 = User.objects.create_user(username='student2', password='12345', type='student')
        # Cria um teste escolar para os testes
        self.test = Test.objects.create(school_test='1', subject=self.subject, class_code=self.subject.class_code, date=datetime.now())
        
    def test_classroom_form_valid_data(self):
        # Testa o formulário ClassroomForm com dados válidos

        # Cria um formulário ClassroomForm com dados válidos
        form = ClassroomForm(data={
            'subject': self.subject.id,
            'date': '2022-01-01',
            'attendance_list': [self.student1.id, self.student2.id],  # Use a lista de IDs de alunos
            'class_diary': 'Math class',
        }, user=self.teacher)

        # Se o formulário não for válido, imprime os erros
        if not form.is_valid():
            print(form.errors)

        # Verifica se o formulário é válido
        self.assertTrue(form.is_valid())

    def test_test_form_valid_data(self):
        # Testa o formulário TestForm com dados válidos

        # Cria um formulário TestForm com dados válidos
        form = TestForm(data={
            'school_test': self.test.school_test,  # Use o valor de school_test do teste criado
            'subject': self.subject.id,
            'class_code': self.subject.class_code.id,  # Use a instância do modelo Class
            'date': '2022-01-01',
        }, user=self.teacher)

        # Se o formulário não for válido, imprime os erros
        if not form.is_valid():
            print(form.errors)

        # Verifica se o formulário é válido
        self.assertTrue(form.is_valid())
        
    def test_grade_form_valid_data(self):
        # Testa o formulário GradeForm com dados válidos

        # Cria um formulário GradeForm com dados válidos
        form = GradeForm(data={
            'grade': 10,
        })

        # Verifica se o formulário é válido
        self.assertTrue(form.is_valid())

    def tearDown(self):
        # Limpeza após o teste. É executado após cada método de teste.
        # Deleta o usuário professor e a matéria criados no setUp
        self.teacher.delete()
        self.subject.delete()


class TestViews(TestCase):
    # Método que é executado antes de cada teste
    def setUp(self):
        # Cria um cliente de teste
        self.client = Client()
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Cria uma turma de teste
        self.class_code = Class.objects.create(code='Test Class', academic_year='2022')
        # Cria uma disciplina de teste
        self.subject = Subject.objects.create(name='Test Subject', teacher=self.user, class_code=self.class_code, slug='required-slug')
        # Cria uma sala de aula de teste
        self.classroom = Classroom.objects.create(subject=self.subject, date=datetime.now(), class_code=self.class_code)
        # Cria um teste de teste
        self.test = Test.objects.create(subject=self.subject, date=datetime.now(), class_code=self.class_code)
        # Cria uma nota de teste
        self.grade = Grade.objects.create(student=self.user, test=self.test, grade=10)
        # Cria um arquivo e associa-o ao ImageField
        image = SimpleUploadedFile(name='test_image.jpg', content=b'some image content', content_type='image/jpeg')
        self.event = Event.objects.create(image=image,title='Test Event', date_time=timezone.now())
        # Cria uma atividade de teste
        self.activity = Activity.objects.create(title='Test Activity', subject=self.subject, delivery_date=datetime.now())

    # Testa a visualização do índice
    def test_index_view(self):
        # Faz uma solicitação GET para a visualização do índice
        response = self.client.get(reverse('main:index'))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

    # Testa a visualização do perfil do usuário
    def test_meu_perfil_view(self):
        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização do perfil do usuário
        response = self.client.get(reverse('main:my-profile'))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

    # Testa a visualização das disciplinas
    def test_disciplinas_view(self):
        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização das disciplinas
        response = self.client.get(reverse('main:subjects'))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)
        
    # Testa a visualização de detalhes do teste
    def test_test_detail_view(self):
        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização de detalhes do teste
        response = self.client.get(reverse('main:grades', args=[self.test.id]))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

    # Testa a visualização de detalhes da atividade
    def test_activity_detail_view(self):
        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização de detalhes da atividade
        response = self.client.get(reverse('main:activities', args=[self.subject.slug]))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

    # Testa a visualização de detalhes do evento
    def test_event_detail_view(self):
        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização de detalhes do evento
        response = self.client.get(reverse('main:event', args=[self.event.id]))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)
        

    # Método que é executado após cada teste
    def tearDown(self):
        # Deleta o usuário de teste
        self.user.delete()
        # Deleta a disciplina de teste
        self.subject.delete()
        # Deleta a sala de aula de teste
        self.classroom.delete()
        # Deleta o teste de teste
        self.test.delete()
        # Deleta a nota de teste
        self.grade.delete()
        # Deleta o evento de teste
        self.event.delete()
        # Deleta a turma de teste
        self.class_code.delete()
        # Deleta a atividade de teste
        self.activity.delete()