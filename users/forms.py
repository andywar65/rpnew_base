from django import forms
from django.forms import ModelForm
from .models import Member, User

class ChangeMemberForm(ModelForm):
    parent = forms.ModelChoiceField(label="Genitore", required = False,
        queryset = User.objects.filter(member__parent = None,
        is_active = True), help_text = 'Solo se minore')

    def clean(self):
        cd = super().clean()
        sector = cd.get('sector')
        parent = cd.get('parent')
        if not sector == '1-YC' and parent:
            self.add_error('sector', forms.ValidationError(
                'Se è minore segue un corso!',
                code='juvenile_follows_course',
            ))

    class Meta:
        model = Member
        fields = '__all__'
