from django.contrib import admin
from .models import Race, Athlete
from .forms import RaceForm, AthleteForm

class AthleteInline(admin.TabularInline):
    model = Athlete
    fields = ('user', 'points', 'placement', 'time')
    extra = 0
    form = AthleteForm

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_date', 'get_location', 'description', )
    inlines = [ AthleteInline, ]
    form = RaceForm