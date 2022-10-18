from pyexpat import model


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AllowedStatus, Employee, Lead, Note,User, Schedule, Status, Sub_Status, Team
# Register your models here.
admin.site.register(Team)
admin.site.register(Lead)
admin.site.register(Status)
admin.site.register(Sub_Status)
admin.site.register(Note)
admin.site.register(Schedule)
admin.site.register(AllowedStatus)
admin.site.register(User)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'current_role',
                    'past_roles', 'joining_date', 'team')



