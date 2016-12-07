from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Skill)
admin.site.register(models.Specialty)