#from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UtenteCreationForm

class SignUpView(CreateView):
    form_class = UtenteCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
