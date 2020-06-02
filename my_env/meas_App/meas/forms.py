from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('Employees_acn', 'Employees_first', 'Employees_last', 'Employees_birthday', 'Employees_phone', 'Employees_mail', 'Employees_vf', 'Employees_vu')
        labels = {
            'Employyes_acn': _('Mitarbeiternummer'),
            'Employees_first': _('Vorname'),
            'Employees_last': _('Nachname'),
            'Employees_birthday': _('Geburtsdatum'),
            'Employees_phone': _('Telefonnummer'),
            'Employees_mail': _('E-mail'),
            'Employees_vf': _('Datensatz gültig von'),
            'Employees_vu': _('Datensatz gültig bis')
        }
        widgets = {
            'Employees_acn': forms.TextInput(attrs={'disabled': True, 'maxlength': 10, 'id': 'id_emplacn', 'required':True, 'class': 'form-control-plaintext input-empledit-form'}),
            'Employees_first': forms.TextInput(attrs={'maxlength': 30, 'id': 'id_emplfirst', 'required':True, 'class': 'form-control input-empledit-form input-req'}),
            'Employees_last': forms.TextInput(attrs={'maxlength': 30, 'id': 'id_empllast', 'required':True, 'class': 'form-control input-empledit-form input-req'}),
            'Employees_birthday': forms.DateInput(attrs={'id': 'id_emplbd', 'class': 'form-control input-empledit-form','type': 'date'}),
            'Employees_phone': forms.TextInput(attrs={'maxlength': 30, 'id': 'id_emplphone', 'class': 'form-control input-empledit-form', 'pattern': '^([0(+][0-9\.-\/ ()]{7,})$'}),
            'Employees_mail': forms.EmailInput(attrs={'id': 'id_emplemail', 'required':True, 'class': 'form-control input-empledit-form input-req', 'type': 'email'}),
            'Employees_vf': forms.DateTimeInput(attrs={'id': 'id_emplvf','required':True, 'class': 'form-control input-empledit-form input-req', 'type': 'datetime-local'}),
            'Employees_vu': forms.DateTimeInput(attrs={'id': 'id_emplvu', 'class': 'form-control input-empledit-form', 'type': 'datetime-local'})
        }

class UploadForm(forms.Form):
    upload_file = forms.FileField(label="", help_text="")
