from django import forms
from .models import *


class DatedImageForm(forms.ModelForm):
    class Meta:
        model = DatedImage
        fields = ['image']
