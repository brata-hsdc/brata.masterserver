from django.contrib import admin
from .models import PiStation, PiEvent

# Register your models here.

@admin.register(PiStation)
class PiStationAdmin(admin.ModelAdmin):
    fieldsets = [("Information", {"fields": [("host", "station_type", "station_id"),
                                             ("last_activity", "joined")]}),
                ]
    list_display = ("host", "station_type", "station_id", "last_activity", "joined")
    ordering = ("host",)
    readonly_fields = ("last_activity", "joined")
    
@admin.register(PiEvent)
class PiEventAdmin(admin.ModelAdmin):
    fieldsets = [("Information", {"fields": [("type", "status", "time"),
                                             "message"]}),
                 ("Relationships", {"fields": ["team",
                                               "pi",]}),
                 ("Data", {"fields": ["data",]})
                ]
    list_filter = ("type", "status", "team", "pi", "time")
    list_display = ("time", "type", "status", "message")
    ordering = ("time",)
    search_fields = ("data", "message")
    readonly_fields = ("time",)
    show_full_result_count = True