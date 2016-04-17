from django import forms

from contentManagement.models import Content


class UploadContentForm(forms.ModelForm):

    class Meta:
        model = Content
        fields = ('title', 'description', 'document', 'is_public')