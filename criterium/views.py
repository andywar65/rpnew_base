from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.views.generic import (DetailView, RedirectView, ListView)
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

class RaceDetailView(DetailView):
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

class RaceListView(ListView):
    model = Race
    ordering = ('date', )
    context_object_name = 'all_races'

    def get_queryset(self):
        year1 = self.kwargs['year']
        year2 = self.kwargs['year2']
        qs = Race.objects.filter(date__gte = datetime(year1, 11, 1),
            date__lt = datetime(year2, 11, 1)).order_by('date')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year']= self.kwargs['year']
        context['year2']= self.kwargs['year2']
        context['year0'] = context['year'] - 1
        context['year3'] = context['year2'] + 1
        female_dict = {}
        male_dict = {}
        for race in context['all_races']:
            athletes = Athlete.objects.filter(race_id=race.id)
            females = athletes.filter(user__member__gender='F')
            males = athletes.filter(user__member__gender='M')
            for female in females:
                if female.user.get_full_name() in female_dict:
                    female_dict[female.user.get_full_name()] += female.points
                else:
                    female_dict[female.user.get_full_name()] = female.points
            for male in males:
                if male.user.get_full_name() in male_dict:
                    male_dict[male.user.get_full_name()] += male.points
                else:
                    male_dict[male.user.get_full_name()] = male.points
        context['females'] = female_dict
        context['males'] = male_dict
        #to be sorted
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
