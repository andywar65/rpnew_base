from django import forms
from django.forms import ModelForm
from .models import UserUpload

class UserUploadForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
        'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)
