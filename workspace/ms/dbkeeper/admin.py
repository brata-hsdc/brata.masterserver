from django.contrib import admin
from .models import Organization, Team, MSUser

# Register your models here.

@admin.register(Organization)
class SchoolAdmin(admin.ModelAdmin):
    pass

@admin.register(MSUser)
class MentorAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
