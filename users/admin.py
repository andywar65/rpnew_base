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
    inlines = [ MemberPaymentInline, ]

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('full', )
