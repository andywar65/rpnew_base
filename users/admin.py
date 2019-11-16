from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail, get_connection
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from .models import User, Member, CourseSchedule, MemberPayment
from .forms import ChangeMemberForm

admin.site.register(User, UserAdmin)

class MemberPaymentInline(admin.TabularInline):
    model = MemberPayment
    fields = ('date', 'amount')
    extra = 1

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = ChangeMemberForm
    list_display = ('get_full_name', 'sector', 'parent', 'mc_state', 'settled')
    list_filter = ('mc_state', 'settled')
    search_fields = ('user__first_name', 'user__last_name',
        'user__username', 'fiscal_code', 'address')
    ordering = ('user__last_name', 'user__first_name', )
    actions = ['control_mc', 'reset_all']
    fieldsets = (
        ('', {'fields':('sector', 'parent')}),
        ('Anagrafica', {'classes': ('grp-collapse grp-closed',),
            'fields':('gender', 'date_of_birth', 'place_of_birth',
            'nationality', 'fiscal_code')}),
        ('Contatti', {'classes': ('grp-collapse grp-closed',),
            'fields':('address', 'phone', 'email_2', )}),
        ('Corso/Tesseramento', {'classes': ('grp-collapse grp-closed',),
            'fields':('course', 'course_alt', 'course_membership',
            'no_course_membership')}),
        ('Uploads', {'classes': ('grp-collapse grp-closed',),
            'fields':('sign_up', 'privacy', 'med_cert',)}),
        ('Amministrazione', {'classes': ('grp-collapse grp-closed',),
            'fields':('membership', 'mc_expiry', 'mc_state', 'total_amount',
            'settled')}),
        )
    inlines = [ MemberPaymentInline, ]

    def control_mc(self, request, queryset):
        if not request.user.has_perm('users.add_user'):
            return
        else:
            for member in queryset:
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
        queryset.update(sign_up='', privacy='', settled='',)
        for member in queryset:
            MemberPayment.objects.filter(member_id = member.pk).delete()
    reset_all.short_description = 'Resetta i dati'

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
                'nationality', 'course', 'course_alt', 'course_membership',
                'no_course_membership', 'sign_up', 'privacy', 'med_cert',])
            if request.user.has_perm('users.add_user'):
                readonly.extend(['membership', 'mc_expiry',
                    'mc_state', 'settled', 'total_amount', ])
        elif member.sector == '1-YC':
            readonly.append('no_course_membership')
        elif member.sector == '2-NC':
            readonly.extend(['course', 'course_alt', 'course_membership', ])
        return readonly

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', )
