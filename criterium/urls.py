from django.urls import path
from .views import (DetailRace, )

app_name = 'criterium'
urlpatterns = [
    path('gara/<slug>/', DetailRace.as_view(),
        name = 'race'),
    ]
