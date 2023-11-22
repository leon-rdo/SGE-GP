from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

User = get_user_model()

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'middle_name', 'email', 'birthdate', 'gender', 'code']
    template_name = 'account/user_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('main:my-profile')