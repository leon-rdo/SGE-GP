from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from .forms import UserRegisterForm

User = get_user_model()

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account_login')
    
    
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'middle_name', 'email', 'birthdate', 'gender', 'code']
    template_name = 'account/user_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('main:my-profile')