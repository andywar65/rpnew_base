from django import forms
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from users.models import (Member, Applicant, UserMessage, )#User,
from users.widgets import SmallClearableFileInput
#from .choices import *

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

class ChangeProfile0Form(ModelForm):

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name', 'email', 'no_spam', )
        widgets = {
            'avatar' : SmallClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email',
                'class': 'form-control'}),
            }

class ChangeProfile3Form(ModelForm):

    class Meta:
        model = Member
        fields = ('avatar', 'first_name', 'last_name',
            'email', 'no_spam',
            'address', 'phone', 'email_2',
            'fiscal_code')
        widgets = {
            'avatar' : SmallClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email',
                'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', }),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email_2': forms.EmailInput(attrs={'autocomplete': 'email',
                'class': 'form-control'}),
            'fiscal_code': forms.TextInput(attrs={'class': 'form-control', }),
            }
