from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from .models import User, Member, Applicant, UserMessage
from .choices import *

class ChangeMemberChildForm(ModelForm):
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
            course = cd.get('course')
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
        fields = ('sector', 'parent',
            'avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled')

class ChangeMember0Form(ModelForm):

    class Meta:
        model = Member
        fields = ('sector',
            'avatar', 'first_name', 'last_name',
            'email', 'no_spam', )

class ChangeMember1Form(ModelForm):

    def clean(self):
        cd = super().clean()
        try:
            course = cd.get('course')
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
        fields = ('sector',
            'avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'email', 'no_spam', 'address', 'phone', 'fiscal_code', 'email_2',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled')

class ChangeMember2Form(ModelForm):

    class Meta:
        model = Member
        fields = ('sector',
            'avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'email', 'no_spam', 'address', 'phone', 'fiscal_code', 'email_2',
            'no_course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled')

class ChangeMember3Form(ModelForm):

    class Meta:
        model = Member
        fields = ('sector',
            'avatar', 'first_name', 'last_name',
            'email', 'no_spam', 'address', 'phone', 'fiscal_code', 'email_2')

class RegistrationForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': 'Nome del genitore', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': 'Cognome del genitore', }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "you@example.com"}))
    sector = forms.ChoiceField(choices = SECTOR,
        widget=forms.Select(attrs={'class': "form-control"}))
    children_str = forms.CharField(required = False,
        widget=forms.TextInput(attrs={'class': "form-control",
        'placeholder': "Nome e cognome figlio 1, nome e cognome figlio 2, ..."}))
    captcha = ReCaptchaField()

    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', 'email', 'sector', 'children_str')

class RegistrationLogForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': 'Nome del figlio', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': 'Cognome del figlio', }))

    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', )

class ContactLogForm(ModelForm):

    class Meta:
        model = UserMessage
        fields = ('user', 'email', 'subject', 'body', 'attachment', 'recipient')
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                'placeholder': "Scrivi qui il messaggio"}), }

class ContactForm(ModelForm):

    captcha = ReCaptchaField()
    
    class Meta:
        model = UserMessage
        fields = ('nickname', 'email', 'subject', 'body')
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "you@example.com"}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                    'placeholder': "Scrivi qui il messaggio"}), }
