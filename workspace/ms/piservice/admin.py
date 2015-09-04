from django.contrib import admin
from .models import PiStation, PiEvent

# Register your models here.

@admin.register(PiStation)
class PiStationAdmin(admin.ModelAdmin):
    pass

@admin.register(PiEvent)
class PiEventAdmin(admin.ModelAdmin):
    pass
