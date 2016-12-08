from django.shortcuts import render

from . import models
#from . import forms

from ProjectsApp.models import Project

# Create your views here.
def getBookmarks(request):
	bookmarked_list = models.Bookmark.objects.all()
	# if Group.objects.get(members=request.user.id) != None:
# 		inGroup = True
# 	else:
# 		inGroup = False
		
	context = {
		
		
		'bookmarks': bookmarked_list,
		
	}
	return render(request, "bookmarks.html")
	
#implement add bookmark function
def addBookmark(request):
	#need to do
	new_bookmark = models.Bookmark()
	new_bookmark.create_bookmark(
		#project_id=models.ForeignKey('ProjectsApp.Project'),
# 		project_id=request.name
# 		need to pass project_id as a parameter but not sure how to
		)
	return render(request, "bookmarks.html")

#implement remove bookmark function
def removeBookmark():
	#need to do
	return NULL
	
