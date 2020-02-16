from datetime import datetime
from django import forms
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget, CheckboxSelectMultiple
from captcha.fields import ReCaptchaField
from users.models import (Member, Applicant, UserMessage, )#User,
from users.widgets import SmallClearableFileInput
from users.choices import *
from users.validators import validate_codice_fiscale

class RegistrationForm(ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', 'email', 'sector', 'children_str')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "Nome del genitore"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "Cognome del genitore"}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "you@example.com"}),
            'sector': forms.Select(attrs={'class': 'form-control',}),
            'children_str': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "Nome e cognome figlio 1, nome e cognome figlio 2, ..."}),}

class RegistrationLogForm(ModelForm):

    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "Nome del figlio"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': "Cognome del figlio"}), }

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

class FrontAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
        'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'class': 'form-control'}),
    )

    def clean(self):
        cd = super().clean()
        try:
            username = cd.get('username')
            user = User.objects.get(username = username)
            if user.member.parent:
                self.add_error(None, forms.ValidationError(
                    """I minori non possono effettuare il login autonomamente!
                    Il loro account è gestito dai genitori.""",
                    code='minor_no_login',
                ))
        except:
            pass

class FrontPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            'class': 'form-control'})
    )

class FrontSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            'class': 'form-control'}),
    )

class FrontPasswordChangeForm(FrontSetPasswordForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'autofocus': True, 'class': 'form-control'}),
    )

class ChangeProfileChildForm(ModelForm):
    gender = forms.CharField( required=True, label='Sesso',
        widget=forms.Select(choices = GENDER, ),)
    date_of_birth = forms.DateField( input_formats=['%d/%m/%Y'], required=False,
        label='Data di nascita (gg/mm/aaaa)',
        widget=SelectDateWidget(years=range(datetime.now().year ,
        datetime.now().year-100, -1), attrs={'class': 'form-control'}))

    def clean(self):
        cd = super().clean()
        try:
            course = cd.get('course')
            course_alt = cd.get('course_alt')
            for sched in course:
                if sched.full == 'Altro' and course_alt == None:
                    self.add_error('course_alt', forms.ValidationError(
                        "Hai scelto 'Altro', quindi scrivi qualcosa!",
                        code='describe_course_alternative',
                    ))
        except:
            pass

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert', )
        widgets = {
            'avatar' : SmallClearableFileInput(),
            'sign_up' : SmallClearableFileInput(),
            'privacy' : SmallClearableFileInput(),
            'med_cert' : SmallClearableFileInput(),
            'course': CheckboxSelectMultiple(),
            }

class ChangeProfile0Form(ModelForm):

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name', 'email', 'no_spam', )
        widgets = {'avatar' : SmallClearableFileInput(),}

class ChangeProfile1Form(ModelForm):
    gender = forms.CharField( required=True, label='Sesso',
        widget=forms.Select(choices = GENDER, ),)
    date_of_birth = forms.DateField( input_formats=['%d/%m/%Y'], required=False,
        label='Data di nascita (gg/mm/aaaa)',
        widget=SelectDateWidget(years=range(datetime.now().year ,
        datetime.now().year-100, -1), attrs={'class': 'form-control'}))

    def clean(self):
        cd = super().clean()
        try:
            course = cd.get('course')
            course_alt = cd.get('course_alt')
            for sched in course:
                if sched.full == 'Altro' and course_alt == None:
                    self.add_error('course_alt', forms.ValidationError(
                        "Hai scelto 'Altro', quindi scrivi qualcosa!",
                        code='describe_course_alternative',
                    ))
        except:
            pass

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'email', 'no_spam',
            'address', 'phone', 'email_2',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert', )
        widgets = {
            'avatar' : SmallClearableFileInput(),
            'sign_up' : SmallClearableFileInput(),
            'privacy' : SmallClearableFileInput(),
            'med_cert' : SmallClearableFileInput(),
            'course': CheckboxSelectMultiple(),
            }

class ChangeProfile2Form(ModelForm):
    gender = forms.CharField( required=True, label='Sesso',
        widget=forms.Select(choices = GENDER, ),)
    date_of_birth = forms.DateField( input_formats=['%d/%m/%Y'], required=False,
        label='Data di nascita (gg/mm/aaaa)',
        widget=SelectDateWidget(years=range(datetime.now().year ,
        datetime.now().year-100, -1), attrs={'class': 'form-control'}))

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'email', 'no_spam',
            'address', 'phone', 'email_2',
            'no_course_membership',
            'sign_up', 'privacy', 'med_cert', )
        widgets = {
            'avatar' : SmallClearableFileInput(),
            'sign_up' : SmallClearableFileInput(),
            'privacy' : SmallClearableFileInput(),
            'med_cert' : SmallClearableFileInput(),
            }

class ChangeProfile3Form(ModelForm):
    fiscal_code = forms.CharField(required=False, label='Codice fiscale',
        validators=[validate_codice_fiscale])

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name',
            'email', 'no_spam',
            'address', 'phone', 'email_2',
            'fiscal_code')
        widgets = {
            'avatar' : SmallClearableFileInput(),
            }
