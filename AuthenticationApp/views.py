"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from . import models
# from UniversitiesApp import models
# from CompaniesApp import models
from . import forms
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser, Student, Professor, Engineer
from UniversitiesApp.models import University
import UniversitiesApp
from CompaniesApp.models import Company
import CompaniesApp
from django.core.handlers.wsgi import WSGIRequest
from StringIO import StringIO


# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'],
			usertype=form.cleaned_data['usertype'],
			about=form.cleaned_data['about'],
			#univ=form.cleaned_data['univ'],
			skills=form.cleaned_data['skills'],
			specialty=form.cleaned_data['specialty'],
			yearsProgramming=form.cleaned_data['yearsprogramming']
			)
		new_user.save()	
		if (new_user.usertype == 'STU'):
			#Also registering students		
			new_student = Student(user = new_user, univ=form.cleaned_data['univ'])
			in_university = University.objects.get(name__exact=form.cleaned_data['univ'].name)
			in_university.members.add(new_user)
			in_university.save();
			new_student.save()
		if (new_user.usertype == 'PRO'):	
			#Also registering professors
			new_professor = Professor(user = new_user, univ=form.cleaned_data['univ'])
			in_university = University.objects.get(name__exact=form.cleaned_data['univ'].name)
			in_university.members.add(new_user)
			in_university.save();
			new_professor.save()
		if (new_user.usertype == 'ENG'):	
			#Also registering engineers
			new_engineer = Engineer(user = new_user, univ=form.cleaned_data['univ'], company=form.cleaned_data['company'])
			in_company = Company.objects.get(name__exact=form.cleaned_data['company'].name)
			in_company.members.add(new_user)
			in_company.save()
			new_engineer.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

def joinUniversityById(request):
    print(request)
    in_id = request.GET.get('name', 'None')
    #changeUniversityJoinedStatus(request, True)
    in_university = models.University.objects.get(name__exact=in_id)
    in_university.members.add(request.user)
    in_university.save();
    request.user.university_set.add(in_university)
    request.user.save()
    context = {
    	'user' : request.user,
        'university' : in_university,
        'userIsMember': True,
    }

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
