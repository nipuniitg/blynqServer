from django import forms

from contentManagement.models import Content


class UploadContentForm(forms.ModelForm):
    #organization_visible = forms.BooleanField()
    class Meta:
        model = Content
        fields = ('title', 'description', 'document')