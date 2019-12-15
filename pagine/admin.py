from django.contrib import admin
from .models import ( Location, ImageEntry, Event,
    EventUpgrade, UserUpload, )
from .forms import LocationForm

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    list_display = ('title', 'address', 'get_thumb', 'get_gmap_link')
    readonly_fields = ('slug', )

@admin.register(ImageEntry)
class ImageEntryAdmin(admin.ModelAdmin):
    list_display = ('get_thumb', 'name', 'description', )
    list_filter = ('date', )
    ordering = ('-date', )
    search_fields = ('description', 'name', )

class EventUpgradeInline(admin.TabularInline):
    model = EventUpgrade
    fields = ('title', 'date', 'body', )
    extra = 0

class UserUploadInline(admin.TabularInline):
    model = UserUpload
    fields = ('user', 'date', 'image', 'body', )
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', )
    inlines = [ EventUpgradeInline, UserUploadInline ]
    search_fields = ('title', 'date', 'intro', )
