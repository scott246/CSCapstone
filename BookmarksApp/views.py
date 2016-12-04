from django.shortcuts import render

# Create your views here.
def getBookmarks(request):
	return render(request, "bookmarks.html")