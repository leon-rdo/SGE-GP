from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .forms import UserRegisterForm
from .models import User


User = get_user_model()


class TestUserViews(TestCase):
    def setUp(self):
        # Configuração inicial do teste. É executado antes de cada método de teste.
        self.client = Client()
        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_register_view(self):
        # Testa a visualização de registro de usuário

        # Faz uma solicitação GET para a visualização de registro de usuário
        response = self.client.get(reverse('account_signup'))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

        # Dados para serem usados na solicitação POST
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        # Faz uma solicitação POST para a visualização de registro de usuário
        response = self.client.post(reverse('account_signup'), data)
        # Verifica se a resposta tem status code 302 (redirecionamento)
        self.assertEqual(response.status_code, 302)

    def test_user_update_view(self):
        # Testa a visualização de atualização de usuário

        # Faz login com o usuário de teste
        self.client.login(username='testuser', password='12345')
        # Faz uma solicitação GET para a visualização de atualização de usuário
        response = self.client.get(reverse('user_update'))
        # Verifica se a resposta tem status code 200 (sucesso)
        self.assertEqual(response.status_code, 200)

        # Dados para serem usados na solicitação POST
        data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'middle_name': 'U',
            'email': 'updateduser@example.com',
            'birthdate': '2000-01-01',
            'gender': 'M',
            'code': '1234',
        }
        # Faz uma solicitação POST para a visualização de atualização de usuário
        response = self.client.post(reverse('user_update'), data)
        # Verifica se a resposta tem status code 302 (redirecionamento)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        # Limpeza após o teste. É executado após cada método de teste.
        # Deleta o usuário de teste
        self.user.delete()


class TestForms(TestCase):
    def test_user_register_form_valid_data(self):
        # Testa o formulário de registro de usuário com dados válidos

        # Cria um formulário de registro de usuário com dados válidos
        form = UserRegisterForm(data={
            'first_name': 'Test',
            'middle_name': 'User',
            'last_name': 'Last',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'birthdate': '2000-01-01',
            'gender': 'M',
            'code': '1234',
            'password1': 'password123',
            'password2': 'password123',
        })

        # Verifica se o formulário é válido
        self.assertTrue(form.is_valid())

    def test_user_register_form_no_data(self):
        # Testa o formulário de registro de usuário sem dados

        # Cria um formulário de registro de usuário sem dados
        form = UserRegisterForm(data={})

        # Verifica se o formulário é inválido
        self.assertFalse(form.is_valid())
        # Verifica se o número de erros é igual ao número de campos no formulário
        self.assertEquals(len(form.errors), 10)

class TestUserModel(TestCase):
    def setUp(self):
        # Configuração inicial do teste. É executado antes de cada método de teste.
        # Cria um usuário de teste
        self.user = User.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            middle_name='Middle',
            birthdate=date(2000, 1, 1),
            gender='M',
            code='1234',
            type='student',
        )

    def test_age(self):
        # Testa o método age do modelo User

        # Assume que o ano atual é 2022
        # Verifica se o método age retorna a idade correta
        self.assertEqual(self.user.age(), 22)

    def test_str(self):
        # Testa o método __str__ do modelo User

        # Verifica se o método __str__ retorna a string correta
        self.assertEqual(str(self.user), 'Test Middle User')

    def tearDown(self):
        # Limpeza após o teste. É executado após cada método de teste.
        # Deleta o usuário de teste
        self.user.delete()