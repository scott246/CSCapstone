"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render, render_to_response

from . import models
from . import forms
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project
import AuthenticationApp

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        is_project = Project.objects.filter(takenBy__exact=in_group).first()
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'selectedProject': is_project,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addMember(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_email = request.POST.get('email', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        try:
            in_member = models.MyUser.objects.get(email__exact=in_email)
        except models.MyUser.DoesNotExist:
            return render(request, 'generalerror.html')
        in_group.members.add(in_member)
        in_group.save();
        in_member.group_set.add(in_group)
        in_member.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')


def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def removeGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')

        in_group = models.Group.objects.get(name=in_name)
        in_group.delete()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'index.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getCommentForm(request):
    comments_list = models.Comment.objects.all()
    context = {
        'comments' : comments_list,
    }
    return render(request, 'comments.html', context)
    
def addComment(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = models.Comment(comment=form.cleaned_data['comment'])
            new_comment.save()
            comments_list = models.Comment.objects.all()
            context = {
                'comments' : comments_list,
            }
            return render(request, 'comments.html', context)
        else:
            form = forms.CommentForm()
    return render(request, 'comments.html')

def removeComment(request):
    comment = models.Comment.objects.get(id=request.GET.get('id', 'None'))
    comment.delete()
    return render(request, 'comments.html')
    
    