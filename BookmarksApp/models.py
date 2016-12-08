from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Bookmark(models.Model):
	def create_bookmark(self, user_id=None, project_id=None):
#		self.user_id = models.ForeignKey('AuthenticationApp.MyUser')
# 		self.project_id = models.ForeignKey('ProjectsApp.Project')
# 		self.save()
# 		return self
		self.user_id = user_id
		self.project_id = project_id
		self.save()
		return self
		
	user = models.ForeignKey('AuthenticationApp.MyUser', default=0)
	project = models.ForeignKey('ProjectsApp.Project', default=0)