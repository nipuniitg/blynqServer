from django.contrib.auth.models import User
from django import forms

from authentication.models import Address
from screenManagement.models import Screen, ScreenSpecs, Group
from djng.forms import NgModelFormMixin, NgModelForm, NgFormValidationMixin



class AddScreenForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm, forms.ModelForm):

    class Meta:
        model = Screen
        fields = ('screen_name', 'address', 'activation_key', 'screen_size', 'aspect_ratio', 'resolution') # Add specifications if needed

    def clean_screen_name(self):
        screen_name = self.cleaned_data['screen_name']
        try:
            # TODO: Get organization details here to validate unique screen_name in an organization instead of globally.
            Screen.objects.get(screen_name=screen_name)
        except:
            return screen_name
        raise forms.ValidationError('Screen name already exists')

    def __init__(self, *args, **kwargs):
        super(AddScreenForm, self).__init__(*args, **kwargs)


class AddScreenLocation(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('building_name', 'address_line1', 'address_line2', 'area', 'landmark', 'city', 'pincode')
    # TODO: Field validation


class AddScreenSpecs(forms.ModelForm):

    class Meta:
        model = ScreenSpecs
        fields = ('brand', 'model_num', 'weight', 'dimensions', 'display_type', 'contrast_ratio', 'wattage', 'additional_details')
    # TODO: Field validation


class AddGroup(NgModelFormMixin, NgFormValidationMixin, NgModelForm, forms.ModelForm):

    class Meta:
        model = Group
        fields = ('group_name', 'description')

