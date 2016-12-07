"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from datetime import datetime
from CompaniesApp.models import Company

class Project(models.Model):
    def create_project(self, name=None, description=None, created_at=str(datetime.now()), updated_at=str(datetime.now()), company=None, languages=None, yearsProgramming=None, specialty=None):
        if not name:
            raise ValueError('Project must have a name')

        #We can safetly create the user
        #Only the email field is required
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.company = company
        self.languages = languages
        self.yearsProgramming = yearsProgramming
        self.specialty = specialty           
        
        self.save()
        return self

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')
    company = models.ForeignKey('CompaniesApp.Company', default=0)
    languages = models.ManyToManyField('SkillsApp.Skill', related_name='languages')
    yearsProgramming = models.CharField(max_length=3, default='0')
    specialty = models.ManyToManyField('SkillsApp.Specialty', related_name='specialty')

    # TODO Task 3.5: Add field for company relationship
    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)

    def __str__(self):
        return self.name