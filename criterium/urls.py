from django.urls import path
from .views import (DetailRace, RaceRedirectView, CorrectRedirectView,
    RaceYearArchiveView)

app_name = 'criterium'
urlpatterns = [
    path('', RaceRedirectView.as_view(), name = 'all_editions'),
    path('<int:year>/', CorrectRedirectView.as_view(), name = 'correct_edition'),
    path('<int:year>-<int:year2>/', RaceYearArchiveView.as_view(), name = 'edition'),
    path('<int:year>-<int:year2>/<slug>/', DetailRace.as_view(), name = 'race'),
    ]
