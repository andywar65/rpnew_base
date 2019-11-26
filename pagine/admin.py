from django.contrib import admin
from .models import (CourseSchedule, Location, ImageEntry, )

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', 'abbrev')
    ordering = ('abbrev', )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'get_thumb', 'get_gmap_link')
    readonly_fields = ('slug', )

@admin.register(ImageEntry)
class ImageEntryAdmin(admin.ModelAdmin):
    list_display = ('get_thumb', 'name', 'description', )
    list_filter = ('date', )
    ordering = ('date', )
    search_fields = ('description', 'name', )
