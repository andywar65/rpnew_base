from django.contrib import admin
from .models import (CourseSchedule2, )

@admin.register(CourseSchedule2)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', 'abbrev')
    ordering = ('abbrev', )
