from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.views.generic import (DetailView, RedirectView)
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, )
from .models import (Race, Athlete, )

def get_edition_years():
    date = datetime.now()
    year = date.year
    month = date.month
    if month >= 11:
        year1 = year
        year2 = year + 1
    else:
        year1 = year - 1
        year2 = year
    return year1, year2

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
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'all_races'
    year_format = '%Y'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year2'] = context['year'] + relativedelta(years=1)
        return context

class RaceRedirectView(RedirectView):
    """redirects simple /criterium/ url to current edition url"""
    def get_redirect_url(self, *args, **kwargs):
        year1, year2 = get_edition_years()
        url = f'/criterium/{year1}-{year2}/'
        return url

class CorrectRedirectView(RedirectView):
    """redirects simple year url to double year url"""
    def get_redirect_url(self, *args, **kwargs):
        year = kwargs['year']
        url = f'/criterium/{year}-{year+1}/'
        return url
