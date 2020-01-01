"""rpnew_prog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from users import views as user_views
from pagine.views import HomeTemplateView

admin.site.site_header = 'Amministrazione RP'
admin.site.site_title = 'Amministrazione RP'

urlpatterns = [
    #path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('registration/', user_views.registration, name='registration'),
    path('contacts/', user_views.contacts, name='contacts'),
    path('', HomeTemplateView.as_view()),
    path('privacy/', TemplateView.as_view(template_name="privacy.html")),
    path('iscrizioni/', TemplateView.as_view(template_name="iscrizioni.html")),
    path('convenzioni/', TemplateView.as_view(template_name="convenzioni.html")),
    path('favicon.ico',
        RedirectView.as_view(url=settings.STATIC_ROOT + 'images/favicon.ico')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('calendario/', include('pagine.urls.events', namespace = 'pagine')),
    path('articoli/', include('pagine.urls.posts', namespace = 'blog')),
    path('luoghi/', include('pagine.urls.locations')),
    path('criterium/', include('criterium.urls', namespace = 'criterium')),
    path('archivio/', include('wordpress.urls', namespace = 'wordpress')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
