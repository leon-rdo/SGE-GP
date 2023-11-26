from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('__str__', 'username', 'type')
    list_display_links = ('__str__', 'username')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'code')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'type')}),
        ('Informações pessoais', {'fields': ('first_name', 'middle_name', 'last_name', 'gender', 'email', 'code')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )