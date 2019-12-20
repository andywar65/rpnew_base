from django.urls import path
from .views import (DetailRace, RaceArchiveIndexView, RaceYearArchiveView)

app_name = 'criterium'
urlpatterns = [
    path('', RaceArchiveIndexView.as_view(), name = 'all_editions'),
    path('<int:year>-<int:year2>/', RaceYearArchiveView.as_view(), name = 'edition'),
    path('<int:year>-<int:year2>/<slug>/', DetailRace.as_view(), name = 'race'),
    ]
