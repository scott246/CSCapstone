from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bookmarks$', views.getBookmarks, name='Bookmarks'),
]