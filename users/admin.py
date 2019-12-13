from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail, get_connection
from django.db.models import Q

from .models import (User, Member, MemberPayment, Applicant,
    ApplicantChild, UserMessage, )
from .forms import ChangeMemberForm

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_active')

admin.site.register(User, UserAdmin)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'subject', )
    ordering = ('-id', )

class ApplicantChildInline(admin.TabularInline):
    model = ApplicantChild
    fields = ('first_name', 'last_name', )
    extra = 1

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'sector', 'children_str',)
    ordering = ('last_name', 'first_name', )
    search = ('last_name', 'first_name', 'children_str',)
    inlines = [ ApplicantChildInline, ]
    actions = ['applicant_to_user', ]

    def applicant_to_user(self, request, queryset):
        group = Group.objects.get(name='Gestione iscrizione')
        for applicant in queryset:
            username = applicant.last_name.lower() + '_' + applicant.first_name.lower()
            try:
                User.objects.get(username=username)
                username += '_2'
            except:
                pass
            password = User.objects.make_random_password()
            hash_password = make_password(password)
            usr = User.objects.create(username = username,
                first_name = applicant.first_name,
                last_name = applicant.last_name, email = applicant.email,
                password = hash_password, is_staff = True, )
            usr.groups.add(group)
            member = Member.objects.get(user_id=usr.id)
            member.sector = applicant.sector
            member.save()
            children = ApplicantChild.objects.filter(parent=applicant.id)
            for child in children:
                chd_username = child.last_name.lower() + '_' + child.first_name.lower()
                hash_password = make_password('rifondazionepodistica')
                chd = User.objects.create(username = chd_username,
                    first_name = child.first_name,
                    last_name = child.last_name, email = applicant.email,
                    password = hash_password, )
                member = Member.objects.get(user_id=chd.id)
                member.sector = '1-YC'
                member.parent = usr
                member.save()
            mail_to = applicant.email
            message = 'Buongiorno \n'
            message += 'potete loggarvi al sito di RP \n'
            message += f'con nome utente = {username} \n'
            message += f'e password = {password} (da cambiare). \n'
            message += 'Una volta loggati potrete gestire la vostra iscrizione. Grazie. \n'
            message += 'Lo staff di RP'
            con = get_connection(settings.EMAIL_BACKEND)
            send_mail(
                'Credenziali di accesso',
                message,
                'no-reply@rifondazionepodistica.it',
                [mail_to, ] ,
                connection = con,
            )
            applicant.delete()
        return
    applicant_to_user.short_description = 'Crea Utenti'

class MemberPaymentInline(admin.TabularInline):
    model = MemberPayment
    fields = ('date', 'amount')
    extra = 1

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = ChangeMemberForm
    list_display = ('get_thumb', 'get_full_name', 'sector', 'parent',
        'mc_state', 'settled')
    list_filter = ('mc_state', 'settled')
    search_fields = ('user__first_name', 'user__last_name',
        'user__username', 'fiscal_code', 'address')
    ordering = ('user__last_name', 'user__first_name', )
    actions = ['control_mc', 'reset_all', 'control_pay']
    fieldsets = (
        ('', {'fields':('sector', 'parent')}),
        ('Anagrafica', {'classes': ('collapse',),
            'fields':('avatar', 'gender', 'date_of_birth', 'place_of_birth',
            'nationality', 'fiscal_code')}),
        ('Contatti', {'classes': ('collapse',),
            'fields':('address', 'phone', 'email_2', )}),
        ('Corso/Tesseramento', {'classes': ('collapse',),
            'fields':('course2', 'course_alt', 'course_membership',
            'no_course_membership')}),
        ('Uploads', {'classes': ('collapse',),
            'fields':('sign_up', 'privacy', 'med_cert',)}),
        ('Amministrazione', {'classes': ('collapse',),
            'fields':('membership', 'mc_expiry', 'mc_state', 'total_amount',
            'settled')}),
        )
        #'grp-collapse grp-closed'
    inlines = [ MemberPaymentInline, ]

    def control_mc(self, request, queryset):
        if not request.user.has_perm('users.add_user'):
            return
        else:
            for member in queryset:
                if member.sector == '0-NO':
                    continue
                if member.mc_state == '0-NF' or member.mc_state == '5-NI':
                    if member.med_cert:
                        member.mc_state = '1-VF'
                        member.save()
                elif member.mc_state == '2-RE':
                    if member.mc_expiry<date.today() + relativedelta(months=1):
                        member.mc_state = '6-IS'
                        member.save()
                    elif member.mc_expiry<date.today():
                        member.mc_state = '3-SV'
                        member.save()
                elif member.mc_state == '6-IS':
                    if member.mc_expiry<date.today():
                        member.mc_state = '3-SV'
                        member.save()
                elif member.mc_state == '4-SI':
                    member.med_cert = None
                    member.mc_expiry = None
                    member.mc_state = '5-NI'
                    member.save()
                    if member.parent:
                        mail_to = member.parent.email
                    else:
                        mail_to = member.user.email
                    message = 'Buongiorno \n'
                    message += f'Il CM/CMA di {member.get_full_name()} '
                    message += 'risulta scaduto o inesistente. \n'
                    message += 'Si prega di rimediare al più presto. Grazie. \n'
                    message += 'Lo staff di RP'
                    con = get_connection(settings.EMAIL_BACKEND)
                    send_mail(
                        'Verifica CM/CMA',
                        message,
                        'no-reply@rifondazionepodistica.it',
                        [mail_to, ] ,
                        connection = con,
                    )
    control_mc.short_description = 'Gestisci CM/CMA'

    def reset_all(self, request, queryset):
        if not request.user.has_perm('users.add_user'):
            return
        queryset.update(sign_up='', privacy='', settled='', total_amount=0.00)
        for member in queryset:
            MemberPayment.objects.filter(member_id = member.pk).delete()
    reset_all.short_description = 'Resetta i dati'

    def control_pay(self, request, queryset):
        if not request.user.has_perm('users.add_user'):
            return
        for member in queryset:
            if member.sector == '0-NO' or member.settled == 'YES':
                continue
            elif member.total_amount == 0.00:
                member.settled = 'VI'
                member.save()
            else:
                paid = 0.00
                payments = MemberPayment.objects.filter(member_id = member.pk)
                for payment in payments:
                    paid += payment.amount
                if paid >= member.total_amount:
                    member.settled = 'YES'
                    member.save()
                else:
                    member.settled = 'NO'
                    member.save()

    control_pay.short_description = 'Controlla i pagamenti'

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(user__is_active = True)
        if not request.user.has_perm('users.add_user'):
            return qs.filter(Q(pk=request.user.pk) | Q(parent=request.user.pk))
        else:
            return qs

    def get_readonly_fields(self, request, member):
        readonly = []
        if not request.user.has_perm('users.add_user'):
            readonly = ['sector', 'parent', 'membership', 'mc_expiry',
                'mc_state', 'settled', 'total_amount', ]
        if member.parent:
            readonly.extend(['address', 'phone', 'email_2',
                'no_course_membership'])
        elif member.sector == '0-NO':
            readonly.extend(['gender', 'date_of_birth', 'place_of_birth',
                'nationality', 'course2', 'course_alt', 'course_membership',
                'no_course_membership', 'sign_up', 'privacy', 'med_cert',])
            if request.user.has_perm('users.add_user'):
                readonly.extend(['membership', 'mc_expiry',
                    'mc_state', 'settled', 'total_amount', ])
        elif member.sector == '1-YC':
            readonly.append('no_course_membership')
        elif member.sector == '2-NC':
            readonly.extend(['course2', 'course_alt', 'course_membership', ])
        return readonly
