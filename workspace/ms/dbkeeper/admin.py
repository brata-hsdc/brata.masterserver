from django.contrib import admin
from django.forms.widgets import Textarea

from .models import Organization, Team, MSUser, Setting
from .team_code import TeamPassCode

# Register your models here.

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(MSUser)
class MSUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fieldsets = [("Info", {"fields": ["name",
                                      "organization",
                                      ("pass_code", "reg_code", "registered")],
                          }),
                 ("Competition Scores", {"fields": ["total_score",
                                                    "total_duration_s"],
                                        }),
                ]
    list_filter = ("organization",)
    list_display = ("name", "organization", "pass_code", "wordCode", "reg_code", "registered", "total_score", "total_duration_s")
    ordering = ("name",)
    search_fields = ("name", "pass_code", "reg_code")
    readonly_fields = ("pass_code", "reg_code", "registered")
    show_full_result_count = True
    
    def wordCode(self, team):
        return TeamPassCode.wordify(team.pass_code)
    
    def save_model(self, request, obj, form, change):
        obj.code = obj.makeTeamCode()
        obj.save()
    
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = [("Setting", {"fields": [("name", "value"), "description"]})]
    list_display = ("name", "value", "description")
    ordering = ("name",)
    search_fields = ("name", "value", "description")
    show_full_result_count = True
    