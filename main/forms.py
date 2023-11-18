from django import forms
from .models import Classroom, Subject


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
        if user is not None:
            self.fields["subject"].queryset = Subject.objects.filter(teacher=user)
