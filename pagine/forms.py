from django import forms
from django.forms import ModelForm
#from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Location

class LocationForm(ModelForm):
    #image = forms.ImageField(widget = CKEditorUploadingWidget)
    class Meta:
        model = Location
        fields = '__all__'
