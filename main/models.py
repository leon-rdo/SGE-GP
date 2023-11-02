from django.db import models

class Disciplina(models.Model):
    nome = models.CharField(max_length=50)
    matriculados = models.ManyToManyField('accounts.User', related_name='matriculados')