from django.shortcuts import render
from django.views.generic import (DetailView, )
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, )
from .models import (Race, )

class DetailRace(DetailView):
    model = Race
    context_object_name = 'race'
    slug_field = 'slug'

class RaceYearArchiveView(YearArchiveView):
    model = Race
    context_object_name = 'edition'

class RaceArchiveIndexView(ArchiveIndexView):
    model = Race
    context_object_name = 'all_editions'
