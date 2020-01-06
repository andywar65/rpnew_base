from django.contrib import admin
from .models import (Convention, ConventionUpload, Society)

class ConventionUploadInline(admin.TabularInline):
    model = ConventionUpload
    fields = ('title', 'upload')
    extra = 0

@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_location', )
    inlines = [ ConventionUploadInline, ]

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('title', )
