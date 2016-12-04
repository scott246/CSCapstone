from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bookmark(models.Model):
    user_id = models.ForeignKey('AuthenticationApp.MyUser')
    project_id = models.ForeignKey('ProjectsApp.Project')