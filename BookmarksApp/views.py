from django.shortcuts import render

from . import models
#from . import forms

from ProjectsApp.models import Project

# Create your views here.
def getBookmarks(request):
	bookmarked_list = models.Bookmark.objects.filter(user=request.user)
	context = {
		'bookmarks': bookmarked_list,
	}
	return render(request, "bookmarks.html", context)
	
#implement add bookmark function
def addBookmark(request):
	new_bookmark = models.Bookmark()
	userid = request.user.id
	projectid = Project.objects.get(name=request.GET.get('name', 'None')).id
	new_bookmark.create_bookmark(
		userid, projectid
		)
	bookmarked_list = models.Bookmark.objects.filter(user=request.user)
	context = {
		'bookmarks': bookmarked_list,
	}
	return render(request, "bookmarks.html", context)

#implement remove bookmark function
def removeBookmark(request):
	bookmark = models.Bookmark.objects.get(user=request.GET.get('id', 'None'))
	bookmark.delete()
	bookmarked_list = models.Bookmark.objects.filter(user=request.user)
	context = {
		'bookmarks': bookmarked_list,
	}
	return render(request, "bookmarks.html", context)
