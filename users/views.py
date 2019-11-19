from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegistrationForm

def registration(request):
    submitted = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/registration?submitted=True')
    else:
        form = RegistrationForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'users/registration.html', {
        'form': form, 'submitted': submitted})
