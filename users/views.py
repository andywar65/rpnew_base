from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from .forms import (RegistrationForm, RegistrationLogForm, ContactForm,
    ContactLogForm, FrontAuthenticationForm, FrontPasswordResetForm,
    FrontSetPasswordForm, FrontPasswordChangeForm, ChangeProfile0Form)
from .models import User, Member

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

class RegistrationFormView(GetMixin, FormView):
    template_name = 'users/registration.html'
    success_url = '/registration?submitted=True'

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return RegistrationLogForm
        else:
            return RegistrationForm

    def form_valid(self, form):
        applicant = form.save(commit=False)
        if 'sector' not in form.fields:
            applicant.parent = self.request.user
            applicant.email = self.request.user.member.email
            applicant.sector = '1-YC'
        applicant.save()
        return super(RegistrationFormView, self).form_valid(form)

class ContactFormView(GetMixin, FormView):
    template_name = 'users/message.html'
    success_url = '/contacts?submitted=True'

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        if 'subject' in self.request.GET:
            initial.update({'subject': self.request.GET['subject']})
        return initial

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return ContactLogForm
        else:
            return ContactForm

    def form_valid(self, form):
        message = form.save(commit=False)
        if self.request.user.is_authenticated:
            message.user = self.request.user
            message.email = self.request.user.member.email
            if 'recipient' in self.request.GET:
                try:
                    recip = User.objects.get(id=self.request.GET['recipient'])
                    message.recipient = recip.member.email
                except:
                    pass
        message.save()
        return super(ContactFormView, self).form_valid(form)

class FrontLoginView(LoginView):
    template_name = 'users/front_login.html'
    form_class = FrontAuthenticationForm

class FrontLogoutView(LogoutView):
    template_name = 'users/front_logout.html'

class FrontPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = FrontPasswordResetForm

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        """
        #email_field_name = UserModel.get_email_field_name()
        active_users = User.objects.filter(**{
            'member__email': email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

class TemplateResetView(TemplateView):
    template_name = 'users/reset_password_done.html'

class FrontPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_password_confirm.html'
    form_class = FrontSetPasswordForm

class TemplateResetDoneView(TemplateView):
    template_name = 'users/reset_done.html'

class TemplateAccountView(LoginRequiredMixin, GetMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['children'] = User.objects.filter(member__parent__id = self.request.user.id ,
            is_active = True)
        return context

class FrontPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = FrontPasswordChangeForm

class FrontPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class ProfileChangeFormView(LoginRequiredMixin, UpdateView):
    model = Member

    def get(self, request, *args, **kwargs):
        member = self.get_object()
        target_id = member.pk
        if member.parent:
            target_id = member.parent.pk
        if request.user.id != target_id:
            raise Http404("User is not authorized to manage this profile")
        return super(ProfileChangeFormView, self).get(request, *args, **kwargs)

    def get_form_class(self):
        member = self.get_object()
        if member.sector == '0-NO':
            return ChangeProfile0Form
        return super(ProfileChangeFormView, self).get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = self.get_object()
        return context

    def get_template_names(self):
        member = self.get_object()
        if member.sector == '0-NO':
            return 'users/profile_change_0.html'
        return super(ProfileChangeFormView, self).get_template_names()

    def get_success_url(self):
        member = self.get_object()
        return f'/accounts/profile/?submitted={member.get_full_name_reverse()}'
