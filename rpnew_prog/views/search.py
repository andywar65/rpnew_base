from django.shortcuts import render
from django.db.models import Q
from pagine.models import (Event, )

def search_results(request):
    success = False
    if 'q' in request.GET:
        q = request.GET['q']
        events = Event.objects.filter(Q(title__icontains=q)|
            Q(intro__icontains=q))
        if events:
            success = True
        return render(request, 'search_results.html', {'search': q,
            'all_events': events, 'success': success})
    else:
        return render(request, 'search_results.html', {'success': success, })
