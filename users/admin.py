from django.contrib import admin
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

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', )
