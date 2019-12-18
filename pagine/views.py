from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
    MonthArchiveView, DayArchiveView, )
from taggit.models import Tag

from .forms import UserUploadForm
from .models import (Location, Event, UserUpload, )

class ListLocation(ListView):
    model = Location
    ordering = ('title', )
    context_object_name = 'all_locations'
    paginate_by = 12

class DetailLocation(DetailView):
    model = Location
    context_object_name = 'location'
    slug_field = 'slug'

class EventArchiveMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'tag' in self.request.GET:
            qs = qs.filter(tags__id=self.request.GET['tag'])
        return qs

class EventArchiveIndexView(EventArchiveMixin, ArchiveIndexView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    allow_empty = True

class EventYearArchiveView(EventArchiveMixin, YearArchiveView):
    model = Event
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    paginate_by = 12
    year_format = '%Y'
    allow_empty = True

class EventMonthArchiveView(EventArchiveMixin, MonthArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    allow_empty = True

class EventDayArchiveView(EventArchiveMixin, DayArchiveView):
    model = Event
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_events'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

class DetailEvent(DetailView):
    model = Event
    context_object_name = 'event'
    slug_field = 'slug'

class UserUploadCreateView(LoginRequiredMixin, CreateView):
    model = UserUpload
    form_class = UserUploadForm

    def get_success_url(self):
        evt = Event.objects.get(id=self.request.GET['id'])
        return evt.get_path() + '/#upload-anchor'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event = Event.objects.get(id=self.request.GET['id'])
        return super().form_valid(form)
