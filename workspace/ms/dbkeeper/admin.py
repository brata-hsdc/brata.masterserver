from django.contrib import admin
from django.forms.widgets import Textarea

from .models import Organization, Team, MSUser
from .team_code import TeamCode

# Register your models here.

@admin.register(Organization)
class SchoolAdmin(admin.ModelAdmin):
    pass

@admin.register(MSUser)
class MentorAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fieldsets = [("Info", {"fields": ["name",
                                      "organization",
                                      ("code",)],
                          }),
                 ("Competition Scores", {"fields": ["total_score",
                                                    "total_duration_s"],
                                        }),
                ]
    list_filter = ("organization",)
    list_display = ("name", "organization", "code", "wordCode", "total_score", "total_duration_s")
    ordering = ("name",)
    search_fields = ("name", "code")
    readonly_fields = ("code",)
    show_full_result_count = True
    
    def wordCode(self, team):
        return TeamCode.wordify(team.code)
    
    def save_model(self, request, obj, form, change):
        obj.code = obj.makeTeamCode()
        obj.save()