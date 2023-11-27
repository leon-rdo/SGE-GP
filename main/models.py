from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    name = models.CharField("Nome", max_length=50)
    syllabus = models.TextField("Ementa", blank=True, null=True)
    class_code = models.ForeignKey(
        "Class", on_delete=models.CASCADE, verbose_name="Turma"
    )
    academic_probation = models.ManyToManyField(
        "accounts.User", related_name="academic_probation", verbose_name="Dependência", blank=True
    )
    teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Professor', blank=True, null=True)
    slug = models.SlugField(max_length=200, editable=False, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name} {self.class_code}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + str(self.class_code)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"


class Class(models.Model):
    LEVELS = (
        ("M", "Maternal"),
        ("J1", "Jardim 1"),
        ("J2", "Jardim 2"),
        ("1", "1ª Ano"),
        ("2", "2ª Ano"),
        ("3", "3ª Ano"),
        ("4", "4ª Ano"),
        ("5", "5ª Ano"),
        ("6", "6ª Ano"),
        ("7", "7ª Ano"),
        ("8", "8ª Ano"),
        ("9", "9ª Ano"),
        ("1M", "1º Ano - Médio"),
        ("2M", "2º Ano - Médio"),
        ("3M", "3º Ano - Médio"),
    )

    code = models.CharField("Código", max_length=10)
    level = models.CharField("Nível", max_length=50, choices=LEVELS)
    enrolled = models.ManyToManyField(
        "accounts.User", related_name="matriculados", verbose_name="Matriculados", blank=True
    )
    academic_year = models.IntegerField("Ano Letivo")

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return self.code + " - " + self.level + " - " + str(self.academic_year)


class Classroom(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Disciplina"
    )
    class_code = models.ForeignKey(
        Class, on_delete=models.CASCADE, verbose_name="Turma"
    )
    date = models.DateField("Data")
    attendance_list = models.ManyToManyField(
        "accounts.User",
        related_name="students_present",
        verbose_name="lista de presença",
    )
    class_diary = models.TextField("Diário de Classe")
    
    def get_absent_students(self):
        all_students = set(self.class_code.enrolled.all())
        present_students = set(self.attendance_list.all())
        absent_students = all_students - present_students
        return absent_students

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return str(self.subject.name) + " - " + str(self.class_code) + " - " + str(self.date)

class Test(models.Model):
    TESTS = (
        ("1", "1ª Avaliação"),
        ("2", "2ª Avaliação"),
        ("3", "3ª Avaliação"),
        ("4", "4ª Avaliação"),
        ("PF", "Prova Final"),
    )

    school_test = models.CharField("Prova", max_length=50, choices=TESTS)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Disciplina"
    )
    class_code = models.ForeignKey(
        Class, on_delete=models.CASCADE, verbose_name="Turma"
    )
    date = models.DateField("Data")

    class Meta:
        verbose_name = "Prova"
        verbose_name_plural = "Provas"

    def __str__(self):
        return self.get_school_test_display() + " de " + self.subject.name + " - " + str(self.class_code)


class Grade(models.Model):
    student = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, verbose_name="Aluno"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Prova")
    grade = models.FloatField("Nota")

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

    def __str__(self):
        return (
            self.student.first_name
            + " - "
            + self.test.school_test
            + " - "
            + self.test.subject.name
            + " - "
            + str(self.test.class_code)
        )


class Activity(models.Model):
    title = models.CharField("Título", max_length=50)
    prompt = models.TextField("Enunciado")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Disciplina"
    )
    image = models.ImageField('Imagem', upload_to='main/activities', blank=True, null=True)
    creation_date = models.DateField("Data de criação", auto_now_add=True)
    delivery_date = models.DateField("Data de entrega")

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def __str__(self):
        return self.title


class Event(models.Model):
    image = models.ImageField('Imagem', upload_to='main/events', blank=True, null=True)
    title = models.CharField("Título", max_length=50)
    description = models.TextField("Descrição")
    date_time = models.DateTimeField("Data e Hora")
    enrolled = models.ManyToManyField(
        "accounts.User", related_name="participants", verbose_name="Participantes", blank=True
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.title