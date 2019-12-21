from django.shortcuts import render
from django.views.generic import (DetailView, )
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, )
from .models import (Race, Athlete, )

class DetailRace(DetailView):
    model = Race
    context_object_name = 'race'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = context['object']
        athletes = Athlete.objects.filter(race_id=race.id)
        context['females'] = athletes.filter(user__member__gender='F').order_by('-points')
        context['males'] = athletes.filter(user__member__gender='M').order_by('-points')
        return context

class RaceYearArchiveView(YearArchiveView):
    model = Race
    context_object_name = 'edition'

class RaceArchiveIndexView(ArchiveIndexView):
    model = Race
    context_object_name = 'all_editions'
