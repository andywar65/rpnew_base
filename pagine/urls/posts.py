from django.urls import path
from pagine.views import ListBlog, DetailBlog

app_name = 'blog'
urlpatterns = [
    path('', ListBlog.as_view(), name='posts'),
    path('<slug>/', DetailBlog.as_view(), name='post'),
    ]
