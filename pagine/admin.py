from django.contrib import admin
from .models import (CourseSchedule2, Location, )

@admin.register(CourseSchedule2)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', 'abbrev')
    ordering = ('abbrev', )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_gmap_link')
