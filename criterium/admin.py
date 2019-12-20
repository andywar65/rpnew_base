from django.contrib import admin
from .models import Race, Athlete

class AthleteInline(admin.TabularInline):
    model = Athlete
    fields = ('user', 'points', 'placement', 'time')
    extra = 0

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date', 'get_location', 'description', )
    inlines = [ AthleteInline, ]
