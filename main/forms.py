from django import forms
from .models import Classroom, Subject, Test, Grade


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ["subject", "class_code", "date", "attendance_list", "class_diary"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "subject": "Disciplina",
            "class_code": "Turma",
            "date": "Data",
            "attendance_list": "Lista de presença",
            "class_diary": "Diário de Classe",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ClassroomForm, self).__init__(*args, **kwargs)
        if user is not None and user.type == "teacher":
            self.fields["subject"].queryset = Subject.objects.filter(teacher=user)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["school_test", "subject", "class_code", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "school_test": "Avaliação",
            "subject": "Disciplina",
            "class_code": "Turma",
            "date": "Data",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        subject = kwargs.pop("subject", None)
        super(TestForm, self).__init__(*args, **kwargs)
        if user is not None and user.type == "teacher":
            self.fields["subject"].queryset = Subject.objects.filter(teacher=user)
        if subject is not None:
            self.fields["subject"].initial = subject
            

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']