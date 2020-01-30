from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from .forms import (RegistrationForm, RegistrationLogForm, ContactForm,
    ContactLogForm)
from .models import User

class RegistrationFormView(FormView):
    template_name = 'users/registration.html'
    success_url = '/registration?submitted=True'

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return RegistrationLogForm
        else:
            return RegistrationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

    def form_valid(self, form):
        applicant = form.save(commit=False)
        if 'sector' not in form.fields:
            applicant.parent = self.request.user
            applicant.email = self.request.user.member.email
            applicant.sector = '1-YC'
        applicant.save()
        return HttpResponseRedirect(self.get_success_url())

#def registration(request):
    #submitted = False
    #if request.method == 'POST':
        #form = RegistrationForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return HttpResponseRedirect('/registration?submitted=True')
    #else:
        #form = RegistrationForm()
        #if 'submitted' in request.GET:
            #submitted = True
    #return render(request, 'users/registration.html', {
        #'form': form, 'submitted': submitted})

def contacts(request):
    submitted = False
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactLogForm(request.POST)
            if form.is_valid():
                mod_form = form.save(commit=False)
                if 'recipient' in request.GET:
                    try:
                        recip = User.objects.get(id=request.GET['recipient'])
                        mod_form.recipient = recip.member.email
                    except:
                        pass
                mod_form.user = request.user
                mod_form.email = request.user.member.email
                mod_form.save()
                return HttpResponseRedirect('/contacts?submitted=True')
        else:
            form = ContactLogForm()
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'users/message-log.html', {
            'form': form, 'submitted': submitted, })
    else:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/contacts?submitted=True')
        else:
            form = ContactForm()
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'users/message.html', {
            'form': form, 'submitted': submitted})
