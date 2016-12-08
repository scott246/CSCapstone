from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bookmarks$', views.getBookmarks, name='Bookmarks'),
    url(r'^bookmarks/add$', views.addBookmark, name='AddBookmark'),
    url(r'^bookmarks/remove$', views.removeBookmark, name='RemoveBookmark'),
]