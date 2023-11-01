from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'code', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'type')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'code')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )