from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# from django.urls import reverse



class User(AbstractUser):
    
    TYPES = (
        ('student', 'Aluno'),
        ('teacher', 'Professor'),
        ('coordinator', 'Coordenador'),
    )
    
    GENDERS = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    
    groups = models.ManyToManyField(Group, blank=True, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuarios')
    middle_name = models.CharField('Nome do meio', max_length=55, blank=True, null=True)
    birthdate = models.DateField('Data de nascimento', blank=True, null=True)
    gender = models.CharField('Sexo', max_length=1, blank=True, null=True, choices=GENDERS)
    code = models.CharField('Matrícula', max_length=15, blank=True, null=True)
    type = models.CharField('Tipo', max_length=11, choices=TYPES)
    
    def age(self):
        if self.birthdate:
            from datetime import date
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None

    def __str__(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(name for name in names if name is not None)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']