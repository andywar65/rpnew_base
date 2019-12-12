from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from pagine.models import Event

urlpatterns = [
    path('', ArchiveIndexView.as_view(model=Event, date_field='date'))
    ]
