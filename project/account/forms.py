from django import forms
from .models import User
from django.core.exceptions import ValidationError

from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'recipient_firstname',
            'recipient_lastname',
            'recipient_phone',
            'city',
            'address',
            'postal_code',
            'number',
            'unit'
        ]
        error_messages = {
            'recipient_firstname': {'required': "First name is required."},
            'recipient_lastname': {'required': "Last name is required."},
            'recipient_phone': {'required': "Phone number is required."},
            'city': {'required': "City is required."},
            'address': {'required': "Address is required."},
            'number': {'required': "House/building number is required."},
        }


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255)
    birth_date = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)


class PasswordForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Current Password")
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, label="Confirm Password")

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("New passwords do not match.")
        return cleaned_data