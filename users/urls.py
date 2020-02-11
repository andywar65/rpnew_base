from django.urls import path
from .views import (FrontLoginView, FrontPasswordResetView, TemplateResetView)

#namespace is '/accounts/'
urlpatterns = [
    path('login/', FrontLoginView.as_view(),
        name='front_login'),
    path('password_reset/', FrontPasswordResetView.as_view(),
        name='front_password_reset'),
    path('password_reset/done/', TemplateResetView.as_view(),
        name='password_reset_done'),
    ]
