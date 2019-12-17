from django import forms
from django.forms import ModelForm
#from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Location, UserUpload

class LocationForm(ModelForm):
    #image = forms.ImageField(widget = CKEditorUploadingWidget)
    class Meta:
        model = Location
        fields = '__all__'

class UserUploadForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control",
        'placeholder': "Scrivi qui il messaggio"}))
    class Meta:
        model = UserUpload
        fields = ('image', 'body',)
