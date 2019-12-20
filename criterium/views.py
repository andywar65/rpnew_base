from django.shortcuts import render
from django.views.generic import (DetailView, )
from .models import (Race, )

class DetailRace(DetailView):
    model = Race
    context_object_name = 'race'
    slug_field = 'slug'
