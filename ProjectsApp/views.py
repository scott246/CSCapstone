"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import models
from .models import Project
from CompaniesApp.models import Company
from . import forms
from .forms import ProjectForm, UpdateForm
from datetime import datetime

def getProjects(request):
	projects_list = models.Project.objects.all()
	if request.user.usertype == 'ENG':
		context = {
			'userInCompany': True,
			'projects': projects_list,
		}
	else:
		context = {
			'userInCompany': False,
			'projects': projects_list,
		}
	return render(request, 'projects.html', context)

def getProject(request):
	return render(request, 'project.html')

def getProjectForm(request):
	if request.user.is_authenticated() and request.user.usertype == 'ENG':
		form = forms.ProjectForm()
		return render(request, 'projectform.html', {'form': form, 'button_value': 'Submit'})
		print request.user.usertype
		print request.user.is_authenticated
	return render(request, 'generalerror.html', context)

def getProjectFormSuccess(request):
	if request.user.is_authenticated() and request.user.usertype == 'ENG':
		if request.method == 'POST':
			form = forms.ProjectForm(request.POST or None)
			if form.is_valid():
				new_project = Project()
				new_project.create_project(
					name=form.cleaned_data['name'], 
					description=form.cleaned_data["description"],
					created_at=str(datetime.now()),
					updated_at=str(datetime.now()),
					company=models.Company.objects.get(members__exact=request.user.id),
					languages=form.cleaned_data['languages'],
					yearsProgramming=form.cleaned_data['yearsProgramming'],
					specialty=form.cleaned_data['specialty'],
					)
				new_project.save()	
				return render(request, 'index.html')

			context = {
				"form": form,
			}
		else:
			form = forms.ProjectForm()
	return render(request, 'generalerror.html')

def updateProject(request):
	if request.user.is_authenticated() and request.user.usertype == 'ENG' and models.Company.objects.get(members__exact=request.user.id) != None:
		form = UpdateForm(request.POST or None, instance=models.Project.objects.get(name=request.GET.get('name', 'None')))
		if form.is_valid():
			form.save()

		context = {
			"form": form,
			"page_name" : "Update",
			"button_value" : "Update",
			"links" : ["logout"],
		}
		return render(request, 'projectform.html', context)
	return render(request, 'generalerror.html')

