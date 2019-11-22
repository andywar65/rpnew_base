from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import (Location, )

class ListLocation(ListView):
    model = Location
    context_object_name = 'all_locations'
    paginate_by = 10

class DetailLocation(DetailView):
    model = Location
    context_object_name = 'location'
    slug_field = 'slug'
