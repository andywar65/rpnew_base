from django import forms
from django.forms import ModelForm
from .models import Member

class ChangeMemberForm(ModelForm):
    parent = forms.ModelChoiceField(label="Genitore", required = False,
        queryset = Member.objects.filter(parent = None),
        help_text = 'Solo se minore')
    class Meta:
        model = Member
        fields = '__all__'
