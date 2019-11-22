from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from .models import Member, User, Applicant, UserMessage
from .choices import *

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
        try:
            course = cd.get('course2')
            course_alt = cd.get('course_alt')
            for sched in course:
                if sched.full == 'Altro' and course_alt == None:
                    self.add_error('course_alt', forms.ValidationError(
                        'Scrivi qualcosa!',
                        code='describe_course_alternative',
                    ))
        except:
            pass

    class Meta:
        model = Member
        fields = '__all__'

class RegistrationForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control",
        'placeholder': "you@example.com"}))
    sector = forms.ChoiceField(choices = SECTOR, widget=forms.Select(attrs={'class': "form-control"}))
    children_str = forms.CharField(required = False,
        widget=forms.TextInput(attrs={'class': "form-control",
        'placeholder': "Nomi e cognomi dei figli da iscrivere, separati da una virgola"}))
    captcha = ReCaptchaField()
    class Meta:
        model = Applicant
        fields = '__all__'

class ContactLogForm(ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
        'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserMessage
        fields = ('user', 'email', 'subject', 'body')

class ContactForm(ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control",
        'placeholder': "you@example.com"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
        'placeholder': "Scrivi qui il messaggio"}))
    captcha = ReCaptchaField()
    class Meta:
        model = UserMessage
        fields = ('nickname', 'email', 'subject', 'body')
