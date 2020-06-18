from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Permission
from .models import *

# Register your models here.
class Meas_UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Meas_User


class Meas_UserAdmin(UserAdmin):
    form = Meas_UserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('Mandant',)}),
    )
admin.site.register(Permission)
admin.site.register(Mandant)
admin.site.register(Currency)
admin.site.register(Meas_User, Meas_UserAdmin)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Customer_Project)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Related_Service)
admin.site.register(Order)
admin.site.register(Appointment)
admin.site.register(Measurement)
admin.site.register(Measurement_Product)
admin.site.register(Timesheet_Type)
admin.site.register(Timesheet)