__author__ = 'Prasanth'
from django.contrib.auth.models import User
from django import forms
from authentication.models import UserDetails
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password(self):
        cleaned_data = self.cleaned_data
        print cleaned_data
        password = cleaned_data['password']
        password2 = cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Passwords doesnt match')
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username already exists')


class UserDetailsForm(forms.ModelForm):
    #mobileNumber = forms.IntegerField(validators=[valMobileNumber])
    mobileNumber = forms.IntegerField()
    class Meta:
        model = UserDetails
        fields = ('organization', 'mobile_number')


# Field Validators
'''
def valMobileNumber(mobileNumber):
    if mobileNumber/ 1000000000 < 1 :
        raise ValidationError('%s is not a valid mobile Number' % mobileNumber)
        '''


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()