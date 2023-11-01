from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# from django.urls import reverse



class User(AbstractUser):
    
    TYPES = (
        ('student', 'Aluno'),
        ('teacher', 'Professor'),
        ('coordinator', 'Coordenador'),
    )
    
    groups = models.ManyToManyField(Group, blank=True, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuarios')
    code = models.CharField('Matrícula', max_length=15, blank=True, null=True)
    type = models.CharField('Tipo', max_length=11, choices=TYPES)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']
    
    '''
    def get_absolute_url(self):
        return reverse('main:profile', args=[self.username])
    '''