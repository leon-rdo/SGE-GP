from django.db import models


class Subject(models.Model):
    name = models.CharField("Nome", max_length=50)
    syllabus = models.TextField("Ementa")
    class_code = models.ForeignKey(
        "Class", on_delete=models.CASCADE, verbose_name="Turma"
    )
    academic_probation = models.ManyToManyField(
        "accounts.User", related_name="academic_probation", verbose_name="Dependência"
    )

    def __str__(self):
        return self.name

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
    level = models.CharField("Nível", max_length=50)
    enrolled = models.ManyToManyField(
        "accounts.User", related_name="matriculados", verbose_name="Matriculados"
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

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return self.subject.name + " - " + self.class_code + " - " + str(self.date)


class Test(models.Model):
    TESTS = (
        ("1", "1ª Avaliação"),
        ("1R", "Recuperação 1"),
        ("2", "2ª Avaliação"),
        ("2R", "Recuperação 2"),
        ("3", "3ª Avaliação"),
        ("3R", "Recuperação 3"),
        ("4", "4ª Avaliação"),
        ("4R", "Recuperação 4"),
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
        return self.school_test + " de " + self.subject.name + " - " + self.class_code


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
            + self.test.class_code
        )


class Activity(models.Model):
    title = models.CharField("Título", max_length=50)
    prompt = models.TextField("Enunciado")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Disciplina"
    )
    creation_date = models.DateField("Data de criação", auto_now_add=True)
    delivery_date = models.DateField("Data de entrega")

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField("Título", max_length=50)
    description = models.TextField("Descrição")
    date_time = models.DateTimeField("Data e Hora")
    enrolled = models.ManyToManyField(
        "accounts.User", related_name="participants", verbose_name="Participantes"
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.title