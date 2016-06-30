from django import forms

__author__ = 'Prasanth'

# All the General forms should go in here


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()