from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from .models import User, Member, CourseSchedule, MemberPayment

admin.site.register(User, UserAdmin)

class MemberPaymentInline(admin.TabularInline):
    model = MemberPayment
    fields = ('date', 'amount')
    extra = 1

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
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
            'fields':('address', 'phone', 'email_2')}),
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
        qs = super().get_queryset(request)
        if not request.user.has_perm('users.add_user'):
            return qs.filter(Q(pk=request.user.pk) | Q(parent=request.user.pk))
        else:
            return qs

    def get_readonly_fields(self, request, member):
        if not request.user.has_perm('users.add_user'):
            return ('sector', 'parent', 'membership', 'mc_expiry', 'mc_state',
                'settled')
        else:
            return ()

    def get_inline_instances(self, request, member):
        if member.sector == '0-NO':
            return ()
        else:
            inline_instances = super().get_inline_instances(request, member)
            return inline_instances

    def get_fieldsets(self, request, member):
        if member.parent:
            fieldsets = (
                ('', {'fields':('sector', 'parent')}),
                ('Anagrafica', {'classes': ('grp-collapse grp-closed',),
                    'fields':('gender', 'date_of_birth', 'place_of_birth',
                    'nationality', 'fiscal_code')}),
                ('Corso/Tesseramento', {'classes': ('grp-collapse grp-closed',),
                    'fields':('course', 'course_alt', 'course_membership',)}),
                ('Uploads', {'classes': ('grp-collapse grp-closed',),
                    'fields':('sign_up', 'privacy', 'med_cert',)}),
                ('Amministrazione', {'classes': ('grp-collapse grp-closed',),
                    'fields':('membership', 'mc_expiry', 'mc_state',
                    'settled')}),
                )
            return fieldsets
        if member.sector == '0-NO':
            fieldsets = (
                ('', {'fields':('sector', 'parent')}),
                ('Contatti', {'classes': ('grp-collapse grp-open',),
                    'fields':('address', 'phone', 'email_2', 'fiscal_code')}),
                )
            return fieldsets
        elif member.sector == '1-YC':
            fieldsets = (
                ('', {'fields':('sector', 'parent')}),
                ('Anagrafica', {'classes': ('grp-collapse grp-closed',),
                    'fields':('gender', 'date_of_birth', 'place_of_birth',
                    'nationality', 'fiscal_code')}),
                ('Contatti', {'classes': ('grp-collapse grp-closed',),
                    'fields':('address', 'phone', 'email_2')}),
                ('Corso/Tesseramento', {'classes': ('grp-collapse grp-closed',),
                    'fields':('course', 'course_alt', 'course_membership',
                    )}),
                ('Uploads', {'classes': ('grp-collapse grp-closed',),
                    'fields':('sign_up', 'privacy', 'med_cert',)}),
                ('Amministrazione', {'classes': ('grp-collapse grp-closed',),
                    'fields':('membership', 'mc_expiry', 'mc_state',
                    'settled')}),
                )
            return fieldsets
        elif member.sector == '2-NC':
            fieldsets = (
                ('', {'fields':('sector', 'parent')}),
                ('Anagrafica', {'classes': ('grp-collapse grp-closed',),
                    'fields':('gender', 'date_of_birth', 'place_of_birth',
                    'nationality', 'fiscal_code')}),
                ('Contatti', {'classes': ('grp-collapse grp-closed',),
                    'fields':('address', 'phone', 'email_2')}),
                ('', {'fields':('no_course_membership', )}),
                ('Uploads', {'classes': ('grp-collapse grp-closed',),
                    'fields':('sign_up', 'privacy', 'med_cert',)}),
                ('Amministrazione', {'classes': ('grp-collapse grp-closed',),
                    'fields':('membership', 'mc_expiry', 'mc_state',
                    'settled')}),
                )
            return fieldsets
        else:
            fieldsets = super().get_fieldsets(request, member)
            return fieldsets

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', )
