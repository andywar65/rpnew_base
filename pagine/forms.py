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
        queryset = User.objects.with_perm('pagine.add_event'), )

    class Meta:
        model = Event
        fields = '__all__'

class BlogForm(ModelForm):
    author = forms.ModelChoiceField(label="Autore", required = False,
        queryset = User.objects.with_perm('pagine.add_blog'), )

    class Meta:
        model = Blog
        fields = '__all__'
