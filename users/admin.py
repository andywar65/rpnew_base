from django.contrib import admin
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
            'fields':('membership', 'mc_expiry', 'mc_state',
            'settled')}),
        )
    inlines = [ MemberPaymentInline, ]

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
                'mc_state', 'settled']
        if member.parent:
            readonly.extend(['address', 'phone', 'email_2',
                'no_course_membership'])
        elif member.sector == '0-NO':
            readonly.extend(['gender', 'date_of_birth', 'place_of_birth',
                'nationality', 'course', 'course_alt', 'course_membership',
                'no_course_membership', 'sign_up', 'privacy', 'med_cert',])
            if request.user.has_perm('users.add_user'):
                readonly.extend(['membership', 'mc_expiry',
                    'mc_state', 'settled'])
        elif member.sector == '1-YC':
            readonly.append('no_course_membership')
        elif member.sector == '2-NC':
            readonly.extend(['course', 'course_alt', 'course_membership', ])
        return readonly

    #def get_inline_instances(self, request, member):
        #if member.sector == '0-NO':
            #return ()
        #else:
            #return super().get_inline_instances(request, member)

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', )
