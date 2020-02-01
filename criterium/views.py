from datetime import datetime
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
        females = athletes.filter(member__gender='F').order_by('-points',
            'member__last_name', 'member__first_name')
        males = athletes.filter(member__gender='M').order_by('-points',
            'member__last_name', 'member__first_name')
        context['females'] = females
        context['males'] = males
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

    def get_athlete_dict(self, athletes):
        athl_dict = {}
        athl_list = athletes.values_list('member_id', flat = True)
        athl_list = list(dict.fromkeys(athl_list))
        for athl in athl_list:
            athlete = athletes.filter(member_id=athl)
            point_sum = sum(athlete.values_list('points', flat = True))
            first = athlete.first()
            athl_dict[first.member.get_full_name_reverse()] = point_sum
        # thanks to https://stackoverflow.com/questions/613183/
        # how-do-i-sort-a-dictionary-by-value
        athl_dict = {k: v for k, v in sorted(athl_dict.items(),
            key=lambda item: item[1], reverse = True)}
        return athl_dict

    def get_status(self, year):
        if datetime(year, 10, 31) > datetime.now():
            return 'provvisoria'
        return 'definitiva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year']= self.kwargs['year']
        context['year2']= self.kwargs['year2']
        context['year0'] = context['year'] - 1
        context['year3'] = context['year2'] + 1
        race_list = context['all_races'].values_list('id', flat = True)
        athletes = Athlete.objects.filter(race_id__in = race_list)
        females = athletes.filter(member__gender = 'F')
        context['females'] = self.get_athlete_dict(females)
        males = athletes.filter(member__gender = 'M')
        context['males'] = self.get_athlete_dict(males)
        context['status'] = self.get_status(context['year2'])
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
