from django import forms
from django.contrib.auth.models import User
from .models import Task, Activity, Column


class TaskMoveForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['column']
        widgets = {
            'column': forms.Select(attrs={'class': 'form-control'})
        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        labels = {
            'title': 'Título',
            'discipline': 'Disciplina/Área',
            'grade_level': 'Nível de Escolaridade',
            'description': 'Descrição',
            'assignee': 'Responsável',
            'column': 'Coluna',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discipline': forms.Select(attrs={'class': 'form-control'}),
            'grade_level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'column': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.all()
        self.fields['assignee'].label_from_instance = lambda obj: obj.get_full_name() or obj.username



class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'discipline', 'grade_level', 'description', 'assignee',]
        labels = {
            'title': 'Título',
            'discipline': 'Disciplina',
            'grade_level': 'Série',
            'description': 'Descrição',
            'assignee': 'Responsável',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discipline': forms.Select(attrs={'class': 'form-control'}),
            'grade_level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = User.objects.all()
        self.fields['assignee'].label_from_instance = lambda obj: obj.get_full_name() or obj.username

    

class ActivityToTaskForm(forms.Form):
    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Atividades'
    )
    column = forms.ModelChoiceField(
        queryset=Column.objects.all(),
        label='Coluna de Destino'
    )