from django.contrib import admin
from .models import School, Team, Mentor

# Register your models here.

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
