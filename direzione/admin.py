from django.contrib import admin
from .models import (Convention, ConventionUpload, Society, Institutional,
    Paragraph)
from .forms import SocietyForm

class ConventionUploadInline(admin.TabularInline):
    model = ConventionUpload
    fields = ('title', 'upload')
    extra = 0

@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_location', )
    inlines = [ ConventionUploadInline, ]
    autocomplete_fields = ['location', ]

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('title', )
    form = SocietyForm
    autocomplete_fields = ['location', ]

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    fields = ('number', 'title', 'body')
    extra = 0

@admin.register(Institutional)
class InstitutionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    #inlines = [ ParagraphInline, ]
