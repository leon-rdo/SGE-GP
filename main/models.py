from django.db import models


class Subject(models.Model):
    
    name = models.CharField(max_length=50)
    enrolled = models.ManyToManyField('accounts.User', related_name='matriculados')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
    

class Class(models.Model):

    code = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    enrolled = models.ManyToManyField('accounts.User', related_name='matriculados')

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return self.description
    
    
class Classroom(models.Model):
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_code = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_list = models.ManyToManyField('accounts.User', related_name='students_present')
    class_diary = models.TextField()
    
    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        
    def __str__(self):
        return self.subject.name + " - " + self.class_code.description + " - " + str(self.date)
    
    
class Test(models.Model):
    
        TESTS = (
            ('1', '1ª Avaliação'),
            ('1R', 'Recuperação 1'),
            ('2', '2ª Avaliação'),
            ('2R', 'Recuperação 2'),
            ('3', '3ª Avaliação'),
            ('3R', 'Recuperação 3'),
            ('4', '4ª Avaliação'),
            ('4R', 'Recuperação 4'),
            ('PF', 'Prova Final'),
        )
        
        school_test = models.CharField(max_length=50, choices=TESTS)
        subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
        class_code = models.ForeignKey(Class, on_delete=models.CASCADE)
        date = models.DateField()
        
        class Meta:
            verbose_name = "Prova"
            verbose_name_plural = "Provas"
            
        def __str__(self):
            return self.school_test + " - " + self.subject.name + " - " + self.class_code.description
        

class Grade(models.Model):
    
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    grade = models.FloatField()
    
    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        
    def __str__(self):
        return self.student.first_name + " - " + self.test.school_test + " - " + self.test.subject.name + " - " + self.test.class_code.description


class Activity(models.Model):
    
    title = models.CharField(max_length=50)
    prompt = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    
    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
    
    def __str__(self):
        return self.title
    
    
class Event(models.Model):
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        
    def __str__(self):
        return self.title