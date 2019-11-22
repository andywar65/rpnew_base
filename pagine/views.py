from django.shortcuts import render
from django.views.generic import ListView

from .models import (Location, )

class ListLocation(ListView):
    model = Location
    context_object_name = 'all_locations'
    paginate_by = 10
