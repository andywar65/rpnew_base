from django.urls import path
from pagine.views import EventArchiveIndexView

urlpatterns = [
    path('', EventArchiveIndexView.as_view(), name = 'event_index'),
    ]
