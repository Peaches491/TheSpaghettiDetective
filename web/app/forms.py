from django.db import models
from django.forms import ModelForm, Form, CharField, ChoiceField
import phonenumbers

from .widgets import CustomRadioSelectWidget, PhoneCountryCodeWidget
from .models import *

class PrinterForm(ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'action_on_failure', 'tools_off_on_pause', 'bed_off_on_pause', 'detective_sensitivity', 'retract_on_pause', 'lift_z_on_pause']
        widgets = {
            'action_on_failure': CustomRadioSelectWidget(choices=Printer.ACTION_ON_FAILURE),
        }

class UserPrefernecesForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_country_code', 'phone_number']
        widgets = {
            'phone_country_code': PhoneCountryCodeWidget()
        }

    def clean_phone_country_code(self):
        phone_country_code = self.cleaned_data['phone_country_code']
        if not phone_country_code.startswith('+'):
            phone_country_code = '+' + phone_country_code
        return phone_country_code

    def clean(self):
        data = self.cleaned_data
        phone_number = (data['phone_country_code'] or '') + (data['phone_number'] or '')
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except phonenumbers.NumberParseException as e:
            self.add_error('phone_number', e)
