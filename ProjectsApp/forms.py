from django import forms
from .models import Project
from SkillsApp.models import Skill, Specialty

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=10000)
    languages = forms.ModelMultipleChoiceField(label="Programming Languages", queryset=Skill.objects.all())
    specialty = forms.ModelMultipleChoiceField(label="Specialty", queryset=Specialty.objects.all())
    yearsProgramming = forms.CharField(label="Years of Programming Required", max_length=3)


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'languages', 'specialty', 'yearsProgramming')
 

