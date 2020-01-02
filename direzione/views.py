from django.shortcuts import render
from django.views.generic import (ListView, DetailView, TemplateView)
from .models import (Convention, ConventionUpload, )

class ConventionListView(ListView):
    model = Convention
    ordering = ('title', )
    context_object_name = 'all_conventions'
    paginate_by = 12

class ConventionDetailView(DetailView):
    model = Convention
    context_object_name = 'conv'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conv = context['object']
        uploads = ConventionUpload.objects.filter(convention_id=conv.id)
        context['uploads'] = uploads
        return context
