from django.urls import path
from pagine.views import (EventArchiveIndexView, EventMonthArchiveView, )

urlpatterns = [
    path('', EventArchiveIndexView.as_view(), name = 'event_index'),
    path('<int:year>/<int:month>/', EventMonthArchiveView.as_view(),
        name = 'event_month'),
    ]
