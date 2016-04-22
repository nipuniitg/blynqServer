from django import forms

from contentManagement.models import Content
from djng.forms import NgModelFormMixin, NgModelForm, NgFormValidationMixin


class UploadContentForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm, forms.ModelForm):
    #organization_visible = forms.BooleanField()
    class Meta:
        model = Content
        fields = ('title', 'description', 'document')