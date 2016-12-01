"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
import AuthenticationApp
from AuthenticationApp.models import MyUser

def getUniversities(request):
	if request.user.is_authenticated():
		universities_list = models.University.objects.all()
		context = {
			'universities' : universities_list,
		}
		return render(request, 'universities.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def getUniversity(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_name)
		is_member = in_university.members.filter(email__exact=request.user.email)
		is_pro = False
		if MyUser.objects.get(email__exact=request.user.email).usertype == 'PRO':
			is_pro = True
		else:
			is_pro = False

		context = {
			'university' : in_university,
			'userIsMember': is_member,
			'userIsProf': is_pro,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def getUniversityForm(request):
	if request.user.is_authenticated():
		return render(request, 'universityform.html')
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.UniversityForm(request.POST, request.FILES)
			if form.is_valid():
				if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
					return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
				new_university = models.University(name=form.cleaned_data['name'], 
											 photo=request.FILES['photo'],  
											 description=form.cleaned_data['description'],
											 website=form.cleaned_data['website'])
				new_university.save()
				context = {
					'name' : form.cleaned_data['name'],
				}
				return render(request, 'universityformsuccess.html', context)
			else:
				return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
		else:
			form = forms.UniversityForm()
		return render(request, 'universityform.html')
	# render error page if user is not logged in
	return render(request, 'autherror.html')

#helper function to alter database (join_university == true means joining a university, false means unjoining)
def changeUniversityJoinedStatus(usertype, uid, university, univid, join_university):
	if usertype == 'STU':
		myuser = AuthenticationApp.models.Student.objects.get(user_id__exact=uid)
	if usertype == 'PRO':
		myuser = AuthenticationApp.models.Professor.objects.get(user_id__exact=uid)
	if usertype == 'ENG':
		return 'error'

	#joining a university while already in a university renders error
	if myuser.univ_id != 0 and join_university == True:
		print 'joined university but was already in a university :('
		return 'error'

	#unjoining a university when you are in a university changes the joined_university variable to false
	elif myuser.univ_id != 0 and join_university == False:
		myuser.univ_id = 0
		myuser.save(update_fields=['univ_id'])
		print 'unjoined university and was in a university :)'

	#joining a university when you aren't already in a university changes the joined_university variable to true
	elif myuser.univ_id == 0 and join_university == True:
		myuser.univ_id = univid
		myuser.save(update_fields=['univ_id']) 
		print 'joined university and was not in a university :)'

	#unjoining a university and not being in a university (shouldnt ever happen)
	elif myuser.univ_id == 0 and join_university == False:
		print 'unjoined a university and was not in a university :('
		return 'error'


def joinUniversity(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		myuser = MyUser.objects.get(id__exact=request.user.id)
		in_university = models.University.objects.get(name__exact=in_name)
		cujs = changeUniversityJoinedStatus(myuser.usertype, request.user.id, in_university, in_university.id, True)
		if cujs == 'error': return render(request, 'generalerror.html')
		in_university.members.add(request.user)
		in_university.save();
		request.user.university_set.add(in_university)
		request.user.save()
		context = {
			'user' : request.user,
			'university' : in_university,
			'userIsMember': True,
		}
		return render(request, 'university.html', context)
	return render(request, 'autherror.html')

def unjoinUniversity(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		myuser = MyUser.objects.get(id__exact=request.user.id)
		in_university = models.University.objects.get(name__exact=in_name)
		cujs = changeUniversityJoinedStatus(myuser.usertype, request.user.id, in_university, in_university.id, False)
		if cujs == 'error': return render(request, 'generalerror.html')
		in_university.members.remove(request.user)
		in_university.save();
		request.user.university_set.remove(in_university)
		request.user.save()
		context = {
			'user' : request.user,
			'university' : in_university,
			'userIsMember': False,
		}
		return render(request, 'university.html', context)
	return render(request, 'autherror.html')
	
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		is_pro = False
		if MyUser.objects.get(email__exact=request.user.email).usertype == 'PRO':
			is_pro = True
		else:
			is_pro = False

		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
			'userIsProf': is_pro,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		myuser = MyUser.objects.get(id__exact=request.user.id)
		if (myuser.usertype != 'PRO'):
			return render(request, 'autherror.html')

		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
		myuser = MyUser.objects.get(id__exact=request.user.id)
		print(myuser.usertype)
		if (myuser.usertype != 'PRO'):
			return render(request, 'autherror.html')

		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				in_university_name = request.GET.get('name', 'None')
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				new_course = models.Course(tag=form.cleaned_data['tag'],
										   name=form.cleaned_data['name'],
										   description=form.cleaned_data['description'],
										   university=in_university)
				new_course.save()
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				return render(request, 'university.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	return render(request, 'autherror.html')
		
def removeCourse(request):
	if request.user.is_authenticated():
		myuser = MyUser.objects.get(id__exact=request.user.id)
		if (myuser.usertype != 'PRO'):
			return render(request, 'autherror.html')

		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def removeStudent(request):
	if request.user.is_authenticated():
		myuser = MyUser.objects.get(id__exact=request.user.id)
		if (myuser.usertype != 'PRO'):
			print(myuser.usertype)
			return render(request, 'autherror.html')

		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_student_email = request.GET.get('student', 'None')
		in_student = in_course.members.filter(email__exact=in_student_email)
		in_course.members.remove(in_student.first())
		context = {
			'university' : in_university,
			'course' : in_course,
			'student' : in_student,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def addStudent(request):
	if request.user.is_authenticated():
		myuser = MyUser.objects.get(id__exact=request.user.id)
		if (myuser.usertype != 'PRO'):
			print(myuser.usertype)
			return render(request, 'autherror.html')

		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_student_email = request.GET.get('student', 'None')
		in_student = in_university.members.filter(email__exact=in_student_email)
		in_course.members.add(in_student.first())
		context = {
			'university' : in_university,
			'course' : in_course,
			'student' : in_student,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
