from django import forms
from django.forms import ModelForm
from .models import UserUpload, Event, Blog
from users.models import User

class UserUploadForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
        'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)

class EventForm(ModelForm):
    manager = forms.ModelChoiceField(label="Responsabile", required = False,
        queryset = User.objects.filter(groups__name = 'Dirigenti',
        is_active = True, ), )

    class Meta:
        model = Event
        fields = '__all__'

class BlogForm(ModelForm):
    author = forms.ModelChoiceField(label="Autore", required = False,
        queryset = User.objects.filter(groups__name = 'Autori',
            is_active = True, ), )

    class Meta:
        model = Blog
        fields = '__all__'
