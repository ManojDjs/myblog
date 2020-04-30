from fractions import Fraction

from camera_imagefield import CameraImageField
from django import forms


class MyForm(forms.Form):
    landscape = CameraImageField(aspect_ratio=Fraction(16, 9))

    class Meta():
        fields = ['landscape']
        widgets = {
            'landscape': forms.fields.TextInput(
                attrs={'placeholder': 'Enter your user name', 'class': 'form-control form-control-sm'})
        }
from django import forms

from .models import Location


class MyModelForm(forms.ModelForm):

    class Meta:
        fields = ('location', 'location_lat', 'location_lon', )
        model = Location