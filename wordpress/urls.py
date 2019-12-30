from django.urls import path
from .views import (wp_list_view, wp_detail_view)

app_name = 'wordpress'
urlpatterns = [
    path('', wp_list_view, name = 'posts'),
    path('<int:id>/', wp_detail_view, name = 'post'),
    ]
