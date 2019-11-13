from django import forms
from django.forms import ModelForm
from .models import Member, User

class ChangeMemberForm(ModelForm):
    parent = forms.ModelChoiceField(label="Genitore", required = False,
        queryset = User.objects.filter(member__parent = None,
        is_active = True), help_text = 'Solo se minore')
    class Meta:
        model = Member
        fields = '__all__'
