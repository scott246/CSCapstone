"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/all$', views.getProjects, name='Projects'),
    url(r'^project$', views.getProject, name='Project'),
    url(r'^project/form$', views.getProjectForm, name='ProjectForm'),
    url(r'^project/success$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
    url(r'^project/update$', views.updateProject, name='ProjectUpdate'),
    url(r'^project/remove$', views.removeProject, name='ProjectRemove'),
    url(r'^project/take$', views.takeProject, name='ProjectTake'),
    url(r'^project/suggested$', views.suggestProject, name='ProjectSuggestion'),
]