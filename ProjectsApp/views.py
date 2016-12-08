"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import models
from .models import Project
from CompaniesApp.models import Company
from GroupsApp.models import Group
from SkillsApp.models import Skill, Specialty
from . import forms
from .forms import ProjectForm, UpdateForm
from datetime import datetime

def getProjects(request):
	projects_list = models.Project.objects.all()
	try:
		Group.objects.get(members=request.user.id)
	except:
		inGroup = False
	else:
		inGroup = True
	if request.user.usertype == 'ENG':
		context = {
			'userInCompany': True,
			'userInGroup': inGroup,
			'projects': projects_list,
		}
	else:
		context = {
			'userInCompany': False,
			'userInGroup': inGroup,
			'projects': projects_list,
		}
	return render(request, 'projects.html', context)

def getProject(request):
	return render(request, 'project.html')

def getProjectForm(request):
	if request.user.is_authenticated() and request.user.usertype == 'ENG':
		form = forms.ProjectForm()
		return render(request, 'projectform.html', {'form': form, 'button_value': 'Submit'})
	return render(request, 'generalerror.html', context)

def getProjectFormSuccess(request):
	if request.user.is_authenticated() and request.user.usertype == 'ENG':
		if request.method == 'POST':
			form = forms.ProjectForm(request.POST, request.FILES)
			# print form
			# print form.is_valid()
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
	# print request.user.is_authenticated()
	# print request.user.usertype
	# print models.Company.objects.get(members=request.user.id)
	# print models.Project.objects.get(name=request.GET.get('name', 'None')).company
	#make sure user is authenticated, is engineer, and belongs to the same company that created the project
	if request.user.is_authenticated() and request.user.usertype == 'ENG' and models.Company.objects.get(members=request.user.id) == models.Project.objects.get(name=request.GET.get('name', 'None')).company:
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
	#return render(request, 'generalerror.html')

def takeProject(request):
	if request.user.is_authenticated():
		if Group.objects.get(members=request.user.id) != None:
			project = Project.objects.get(name=request.GET.get('name', 'None'))
			in_group = Group.objects.get(members=request.user.id)
			# print project.takenBy
			# if project.takenBy != 0:
			#  	return render(request, 'generalerror.html')
			in_group.project = models.Project.objects.get(name=request.GET.get('name', 'None'))
			in_group.save()
			project.takenBy = in_group
			project.save()
			context = {
				'userInGroup': True
			}
			return render(request, 'index.html')
	return render(request, 'autherror.html')

def skillsAreEqual(skill1, skill2):
	if skill1.name == skill2.name:
		return True
	return False

def projectInList(list1, project):
	for thingus in list1:
		if thingus.name == project.name:
			return True
	return False

#project matching system
def suggestProject(request):
	if request.user.is_authenticated():
	 	projects_list = models.Project.objects.all()
	 	group = Group.objects.get(members=request.user.id)
	 	members = group.members.all()
	 	totalSkills = list()
	 	totalSpecialties = list()
	 	lowestYearsProgramming = 999
	 	suggestedList = list()

	 	#takes combined members' skills and specialties...
	 	for member in members:
	 		memberSkills = list(member.skills.all())
	 		memberSpecialties = list(member.specialty.all())
			totalSkills.extend(memberSkills)
			totalSpecialties.extend(memberSpecialties)
			#members with the lowest number of years dictate the entire group's years of experience
			memberYears = int(member.yearsProgramming)
			if memberYears < lowestYearsProgramming:
				lowestYearsProgramming = memberYears

		#...and if a project contains any of these skills/specialties, it's added to the suggestion list
		for project in projects_list:
			projectLanguages = list(project.languages.all())
	 		projectSpecialty = list(project.specialty.all())
	 		projectYears = int(project.yearsProgramming)
			for skill in totalSkills:
				for language in projectLanguages:	
					if (skillsAreEqual(skill, language)) and (projectYears <= lowestYearsProgramming):
						if (projectInList(suggestedList, project) == False):
							suggestedList.append(project)
			for specialty in totalSpecialties:
				for pSpecialty in projectSpecialty:
					if (skillsAreEqual(specialty, pSpecialty)) and (projectYears <= lowestYearsProgramming):
						if (projectInList(suggestedList, project) == False):
							suggestedList.append(project)
		context = {
			'projects': suggestedList,
		}
		return render(request, 'projectsuggestions.html', context)
	return render(request, 'autherror.html')

def removeProject(request):
	if request.user.is_authenticated():
		if (models.Project.objects.get(name=request.GET.get('name', 'None')).company == models.Company.objects.get(members=request.user.id)):
			in_project = models.Project.objects.get(name=request.GET.get('name', 'None'))
			in_project.delete()
			context = {
				'project' : in_project,
				'userInCompany': True,
			}
			return render(request, 'index.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

