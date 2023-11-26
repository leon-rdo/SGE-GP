from django.urls import path, include
from accounts.views import UserRegisterView, UserUpdateView


urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="account_signup"),
    path('', include('allauth.urls')),
    path('accounts/atualizar/', UserUpdateView.as_view(), name='user_update')
]