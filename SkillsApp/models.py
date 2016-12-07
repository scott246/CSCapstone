from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Skill(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):              #Python 3
		return self.name

	def __unicode__(self):           # Python 2
		return self.name

class Specialty(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):              #Python 3
		return self.name

	def __unicode__(self):           # Python 2
		return self.name