from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UtenteCreationForm, UtenteChangeForm
from .models import Utente

class UtenteAdmin(UserAdmin):
    add_form = UtenteCreationForm
    form = UtenteChangeForm
    model = Utente
    list_display = ['email', 'username',]

admin.site.register(Utente, UtenteAdmin)
