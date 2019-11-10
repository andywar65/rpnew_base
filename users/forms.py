from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utente

class UtenteCreationForm(UserCreationForm):

    class Meta:
        model = Utente
        fields = ('username', 'email')

class UtenteChangeForm(UserChangeForm):

    class Meta:
        model = Utente
        fields = ('username', 'email')
