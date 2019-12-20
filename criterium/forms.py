from django import forms
from django.forms import ModelForm
from .models import Race
from pagine.models import Event

class RaceForm(ModelForm):
    event = forms.ModelChoiceField(label="Event", required = False,
        queryset = Event.objects.filter(tags__name__in = ['criterium'], ), )

    class Meta:
        model = Race
        fields = '__all__'
