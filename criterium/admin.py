from django.contrib import admin
from .models import Race

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date', 'get_location', 'description', )
