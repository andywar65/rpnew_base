from django import forms
from django.shortcuts import render
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from pagine.models import (Event, Blog, UserUpload)
from streamblocks.models import (IndexedParagraph, )

class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)

def search_results(request):
    success = False
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = request.GET['q']
        #event content type
        ev_type = ContentType.objects.get(app_label='pagine', model='event').id
        #prepare list of indexed paragraphs containing query
        paragraphs = IndexedParagraph.objects.filter(Q(body__icontains = q)|
            Q(title__icontains = q))
        #filter them by event type
        ev_paragraphs = paragraphs.filter( parent_type = ev_type )
        #extract list of events
        ev_list = ev_paragraphs.values_list('parent_id', flat = True)
        #prepare list of user uploads referenced by events
        uploads = UserUpload.objects.filter(body__icontains = q)
        up_list = uploads.values_list('event_id', flat = True)
        events = Event.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = up_list)|Q(id__in = ev_list))
        if events:
            success = True
        #blog content type
        bl_type = ContentType.objects.get(app_label='pagine', model='blog').id
        #filter paragraphs by blog type
        bl_paragraphs = paragraphs.filter( parent_type = bl_type )
        #extract list of blogs
        bl_list = bl_paragraphs.values_list('parent_id', flat = True)
        #prepare list of user uploads referenced by blog posts
        up_list = uploads.values_list('post_id', flat = True)
        blogs = Blog.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(id__in = up_list)|Q(id__in = bl_list))
        if blogs:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_events': events, 'all_blogs': blogs, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
