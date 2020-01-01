from django.shortcuts import render
from django.db.models import Q
from pagine.models import (Event, Blog, )

def search_results(request):
    success = False
    if 'q' in request.GET:
        q = request.GET['q']
        events = Event.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(body__icontains=q)|
            Q(chronicle__icontains=q)|Q(restricted__icontains=q))
        if events:
            success = True
        blogs = Blog.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q)|Q(body__icontains=q))
        if blogs:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_events': events, 'all_blogs': blogs, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
