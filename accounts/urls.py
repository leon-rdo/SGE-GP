from django.urls import path, include
from accounts.views import UserUpdateView


urlpatterns = [
    path('', include('allauth.urls')),
    path('accounts/atualizar/', UserUpdateView.as_view(), name='user_update')
]