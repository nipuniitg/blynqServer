from django.contrib.auth.models import User
from django import forms
from authentication.models import UserDetails, RequestedQuote
from djng.forms import NgModelForm, NgFormValidationMixin, NgModelFormMixin
from django.core.exceptions import ValidationError


# class UserDetailsForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = UserDetails
#         fields = ('organization', 'mobile_number', 'role')
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             UserDetails.objects.get(username = username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError('Username already exists')
#
#     def clean(self):
#         cleaned_data = super(UserDetailsForm, self).clean()
#         password = cleaned_data['password']
#         confirm_password = cleaned_data['confirm_password']
#         if password != confirm_password:
#              raise forms.ValidationError('Passwords doesnt match')
#         return cleaned_data


class RequestQuoteForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm, forms.ModelForm):

    class Meta:
        model = RequestedQuote
        fields = ('name', 'email', 'mobile_number', 'num_of_devices', 'additional_details')


# Field Validators
'''
def valMobileNumber(mobileNumber):
    if mobileNumber/ 1000000000 < 1 :
        raise ValidationError('%s is not a valid mobile Number' % mobileNumber)
        '''
