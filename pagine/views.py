from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, )

from .models import (Location, Event)

class ListLocation(ListView):
    model = Location
    ordering = ('title', )
    context_object_name = 'all_locations'
    paginate_by = 12

class DetailLocation(DetailView):
    model = Location
    context_object_name = 'location'
    slug_field = 'slug'

class EventArchiveIndexView(ArchiveIndexView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12

class EventYearArchiveView(YearArchiveView):
    model = Event
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    year_format = '%Y'
    allow_empty = True

class EventMonthArchiveView(MonthArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    month_format = '%m'
    allow_empty = True

class DetailEvent(DetailView):
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'
