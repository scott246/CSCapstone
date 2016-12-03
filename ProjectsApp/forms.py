from django import forms
from .models import Project

SKILLS = (
    ('C', 'C'),
    ('JAV', 'Java'),
    ('C++', 'C++'),
    ('PYT', 'Python'),
    ('HTM', 'HTML/CSS'),
    ('SQL', 'SQL'),
    ('RUB', 'Ruby'),
    ('JS', 'JavaScript'),
    ('C#', 'C#'),
    ('PHP', 'PHP'),
)

SPECIALTIES = (
	('WIN', 'Windows'),
	('MAC', 'Macintosh'),
	('IOS', 'iOS'),
	('AND', 'Android'),
	('WEB', 'Web Development'),
	('CVN', 'Computer Vision'),
	('AI', 'AI'),
	('BIG', 'Big Data'),
)

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=10000)
    languages = forms.MultipleChoiceField(label="Programming Languages", choices=SKILLS)
    specialty = forms.MultipleChoiceField(label="Specialty", choices=SPECIALTIES)
    yearsProgramming = forms.CharField(label="Years of Programming Required", max_length=3)


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'languages', 'specialty', 'yearsProgramming')
 

